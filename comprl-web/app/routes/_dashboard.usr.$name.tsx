import { Typography, Stack } from "@mui/material";
import { LoaderFunctionArgs, redirect } from "@remix-run/node";
import { authenticator } from "~/services/auth.server";
import { commitSession, getSession } from "~/services/session.server";
import { useLoaderData } from "@remix-run/react";
import DashboardContent from '~/components/DashboardContent';



export async function loader({ request, params }: LoaderFunctionArgs) {
  const user = await authenticator.isAuthenticated(request, {
    failureRedirect: "/login",
  });

  const session = await getSession(request.headers.get("Cookie"));

  if (params.name !== user.name) {

    session.flash("popup", { message: "You don't have permission to access that page", severity: "error" });

    return redirect(`/usr/${user.name}`, {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    });
  }

  if (!user.token) {
    return { token: "no token exists" };
  }

  return { token: user.token, username: user.name };
}

export default function UserDashboard() {
  const { token, username } = useLoaderData<typeof loader>();
  return (
    <div>
    <Stack
      direction = {{xs: 'column', sm: 'row'}}
      spacing={{xs:1, sm:2, md:4}}
    >
      <DashboardContent caption="Username" children={username}/>
      <DashboardContent caption="Token" children={token}/>
    </Stack>
    </div>
  );
}