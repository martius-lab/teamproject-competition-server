import { Box, Button, Link, TextField, Typography } from "@mui/material";
import { ActionFunctionArgs } from "@remix-run/node";
import { Form } from "@remix-run/react";
import { USERNAME_PASSWORD_STRATEGY, authenticator } from "~/services/auth.server";


export async function action({ request }: ActionFunctionArgs) {



  return await authenticator.authenticate(USERNAME_PASSWORD_STRATEGY, request, {
    successRedirect: "/dashboard",
    failureRedirect: "/login",
  });
}

export default function Login() {

  return (
    <Form method="POST">
      <Typography align="center" variant="h5">Sign In</Typography>
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
      <Box
        mt={2}
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          typography: 'body1',
        }}>
          <Typography mr={1}>Not a member?</Typography>
          <Link href="/register" sx={{ display: 'block', textAlign: 'center' }}>Create an account</Link>
      </Box>
    </Form>
  );
}