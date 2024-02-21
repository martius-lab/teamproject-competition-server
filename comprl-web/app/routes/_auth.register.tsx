import { Box, Button, Link, TextField, Typography } from "@mui/material";
import { ActionFunctionArgs } from "@remix-run/node";
import { Form } from "@remix-run/react";
import { addUser } from "~/db/sqlite.data";
import { USERNAME_PASSWORD_STRATEGY, authenticator } from "~/services/auth.server";

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData()

  addUser(formData.get("username") as string, formData.get("password") as string);

  return await authenticator.authenticate(USERNAME_PASSWORD_STRATEGY, request, {
    successRedirect: "/dashboard",
    context: { formData },
  });
}

export default function Login() {

  return (
    <Form method="POST">
      <Typography align="center" variant="h5">Sign Up</Typography>
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
      <TextField
        margin="normal"
        required
        fullWidth
        label="Key"
        type="password"
        name="key"
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
      >
        Create Account
      </Button>
      <Box
        mt={2}
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          typography: 'body1',
        }}>
        <Typography mr={1}>Already have an account?</Typography>
        <Link href="/login" sx={{ display: 'block', textAlign: 'center' }}>Sign-In</Link>
      </Box>
    </Form>
  );
}