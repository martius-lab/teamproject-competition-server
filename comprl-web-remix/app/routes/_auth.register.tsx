import { Alert, AlertColor, Box, Button, Link, TextField, Typography } from "@mui/material";
import { ActionFunctionArgs, redirect } from "@remix-run/node";
import { Form, useActionData } from "@remix-run/react";
import { useState } from "react";
import { addUser } from "~/db/sqlite.data";
import { config } from "~/config";

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData()
  const key = formData.get("key") as string;
  const username = formData.get("username") as string;
  const password = formData.get("password") as string;

  if (key !== config.Web.key) {
    return {
      alerts: [{ severity: "error", message: "Invalid key" }]
    }
  }

  try {
    await addUser(username, password);
  } catch (error) {
    return {
      alerts: [{ severity: "error", message: error.message }]
    }
  }
  return redirect("/login");
}

export default function Register() {
  const data = useActionData<typeof action>();

  const [password, setPassword] = useState("");
  const [repeatPassword, setRepeatPassword] = useState("");

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
        onChange={(e) => setPassword(e.target.value)}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        label="Repeat Password"
        type="password"
        name="repeatPassword"
        onChange={(e) => setRepeatPassword(e.target.value)}
        error={password !== repeatPassword}
        helperText={password !== repeatPassword ? "Passwords do not match" : ""}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        label="Key"
        type="password"
        name="key"
      />
      {data?.alerts?.map((alert, i) =>
        <Alert sx={{ mt: 1 }} key={i} severity={alert.severity as AlertColor}>{alert.message}</Alert>
      )}
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 1 }}
      >
        Create Account
      </Button>
      <Box
        m={2}
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
