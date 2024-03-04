import { LoaderFunctionArgs } from "@remix-run/node"
import { authenticator } from "~/services/auth.server";

export async function loader({request}: LoaderFunctionArgs) {
    await authenticator.logout(request, { redirectTo: "/login" });
}