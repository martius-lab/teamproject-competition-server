import { Typography } from "@mui/material";
import { LoaderFunctionArgs, redirect } from "@remix-run/node";
import { authenticator } from "~/services/auth.server";
import { commitSession, getSession } from "~/services/session.server";
import { getToken } from "~/db/sqlite.data";
import { useLoaderData } from "@remix-run/react";



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

  return { token: user.token };
}

export default function UserDashboard() {
  const { token } = useLoaderData<typeof loader>();
  return (
    <>
      <Typography variant="h1">User</Typography>
      <Typography variant="body1">Token: {token}</Typography>
    </>
  );
}