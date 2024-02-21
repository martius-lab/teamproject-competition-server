import { Authenticator } from "remix-auth";
import { sessionStorage } from "~/services/session.server";
import { FormStrategy } from "remix-auth-form";

interface User {
    id: number;
    name: string;
    //email: string;
    role: "admin" | "user";
}

// Create an instance of the authenticator, pass a generic with what
// strategies will return and will store in the session
export const authenticator = new Authenticator<User>(sessionStorage);

authenticator.use(
    new FormStrategy(async ({ form }) => {
        console.log(form.get("username"));
        console.log(form.get("password"));

        //const name = form.get("username");
        //const password = form.get("password");
        // here you would check the credentials against your database

        // the type of this user must match the type you pass to the Authenticator
        // the strategy will automatically inherit the type if you instantiate
        // directly inside the `use` method
        return { id: 1, name: "TestUser", role: "admin"};
    }),
    // each strategy has a name and can be changed to use another one
    // same strategy multiple times, especially useful for the OAuth2 strategy.
    "LOGIN_USERNAME_PASSWORD"
);