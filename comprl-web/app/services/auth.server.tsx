import { Authenticator, AuthorizationError } from "remix-auth";
import { sessionStorage } from "~/services/session.server";
import { FormStrategy } from "remix-auth-form";
import { getUser } from "~/db/sqlite.data";
import User from "~/db/types";

// Create an instance of the authenticator, pass a generic with what
// strategies will return and will store in the session
export const authenticator = new Authenticator<User>(sessionStorage);
export const USERNAME_PASSWORD_STRATEGY = "USERNAME_PASSWORD_STRATEGY";

authenticator.use(
    new FormStrategy(async ({ form }) => {

        const name = form.get("username")?.toString() ?? "";
        const password = form.get("password")?.toString() ?? "";
        //const password = form.get("password");
        
        //TODO: implement password hashing, and better authentication
        const user: User = await getUser(name, password);
        if (!user) {
            throw new AuthorizationError("Invalid username or password");
        }

        // the type of this user must match the type you pass to the Authenticator
        // the strategy will automatically inherit the type if you instantiate
        // directly inside the `use` method
        return user;
    }),
    // each strategy has a name and can be changed to use another one
    // same strategy multiple times, especially useful for the OAuth2 strategy.
    USERNAME_PASSWORD_STRATEGY
);