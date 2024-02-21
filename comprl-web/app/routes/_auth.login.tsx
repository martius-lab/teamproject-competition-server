import { Button, TextField, Typography } from "@mui/material";
import { ActionFunctionArgs } from "@remix-run/node";
import { useNavigate } from "@remix-run/react";
import { authenticator } from "~/services/auth.server";


export async function action({ request }: ActionFunctionArgs) {
  return await authenticator.authenticate("LOGIN_USERNAME_PASSWORD", request, {
    successRedirect: "/dashboard",
    failureRedirect: "/login",
  });
}

export default function Login() {

  const navigate = useNavigate()

  return (
    <form method="POST">
      <Typography align="center" variant="h5">Login</Typography>
      <TextField
        margin="normal"
        required
        fullWidth
        label="Username"
        name="username"
      />
      <TextField
        margin="normal"
        required
        fullWidth
        label="Password"
        type="password"
        name="password"
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
      >
        Sign In
      </Button>
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        onClick={() => navigate("/register")}
      >
        Register new User
      </Button>
    </form>
  );
}