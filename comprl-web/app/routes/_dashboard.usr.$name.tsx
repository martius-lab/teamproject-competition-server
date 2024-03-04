import { Typography } from "@mui/material";
import { LoaderFunctionArgs, redirect } from "@remix-run/node";
import { authenticator } from "~/services/auth.server";
import { commitSession, getSession } from "~/services/session.server";



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

  return {}
}

export async function action({ request }: ActionFunctionArgs) {
  console.log('Usr');
  return {}
}


export default function UserDashboard() {

  return (
    <Typography variant="h1">User</Typography>
  );
}