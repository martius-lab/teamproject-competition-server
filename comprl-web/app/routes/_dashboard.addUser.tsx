import * as React from 'react';
import { Box, Typography, Button, TextField, MenuItem, InputLabel, SelectChangeEvent, NativeSelect } from "@mui/material";
import { ActionFunctionArgs, LoaderFunctionArgs, redirect } from "@remix-run/node";
import { Form } from "@remix-run/react";
import { authenticator } from "~/services/auth.server";
import { commitSession, getSession } from "~/services/session.server";
import { addUser} from "~/db/sqlite.data";

export async function loader({ request, params }: LoaderFunctionArgs) {
  const user = await authenticator.isAuthenticated(request, {
    failureRedirect: "/login",
  });

  const session = await getSession(request.headers.get("Cookie"));

  // TODO admin role check
  //if (params.role != "admin") {
  if (false) {

    session.flash("popup", { message: "You don't have permission to access that page", severity: "error" });

    return redirect(`/usr/${user.name}`, {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    });
  }

  return { };
}

export async function action({ request }: ActionFunctionArgs) {
    const formData = await request.formData()
    const username = formData.get("username") as string;
    const password = formData.get("password") as string;
    const role = formData.get("role") as string;
  
    try {
      console.log("Adding")
      await addUser(username, password, role);
      console.log("Added")
    } catch (error) {
      return {
        alerts: [{ severity: "error", message: "Username is already taken" }]
      }
    }
    return redirect("/admin");
}

export default function AdminAddUser() {
  return (
    <div>
      <Box sx={{ height: 500, width: 500 }} >
        <Typography variant="h4">Add User:</Typography>
        <Form method="POST">
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
            name="password"
          />
          <InputLabel variant="standard" htmlFor="uncontrolled-native">Role:</InputLabel>
          <NativeSelect
            inputProps={{
              name: "role",
              required: true,}}
            defaultValue={'user'}
          >
            <option value={'user'}>User</option>
            <option value={'admin'}>Admin</option>
            <option value={'bot'}>Bot</option>
          </NativeSelect>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 1 }}
          >
            Add user
          </Button>
        </Form>
      </Box>
    </div>
  )
}
