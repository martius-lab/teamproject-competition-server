import { Alert, AlertColor, Box, Button, Link, TextField, Typography } from "@mui/material";
import { ActionFunctionArgs } from "@remix-run/node";
import { Form, useActionData } from "@remix-run/react";
import { AuthorizationError } from "remix-auth";
import { USERNAME_PASSWORD_STRATEGY, authenticator } from "~/services/auth.server";


export async function action({ request }: ActionFunctionArgs) {
  try {
    return await authenticator.authenticate(USERNAME_PASSWORD_STRATEGY, request, {
      successRedirect: "/dashboard",
      throwOnError: true,
    });
  } catch (error) {
    if (error instanceof Response) return error;
    if (error instanceof AuthorizationError) {
      return {
        alerts: [{ severity: "error", message: error.message }]
      }
    }
  }
}

export default function Login() {
  const data = useActionData<typeof action>();
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
      {data?.alerts?.map((alert, i) => <Alert sx={{ mt: 1 }} key={i} severity={alert.severity as AlertColor}>{alert.message}</Alert>)}
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