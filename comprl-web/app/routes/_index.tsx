import { type MetaFunction, type LoaderFunctionArgs, redirect } from "@remix-run/node";
import { authenticator } from "~/services/auth.server";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export async function loader({ request }: LoaderFunctionArgs) {

  const user = await authenticator.isAuthenticated(request, {
    failureRedirect: "/login",
  });

  return redirect(`/usr/${user?.name}`);
}
