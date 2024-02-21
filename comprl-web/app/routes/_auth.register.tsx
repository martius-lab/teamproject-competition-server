import { Box, Button, Link, TextField, Typography } from "@mui/material";
import { useState } from "react";

export default function Login() {

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [key, setLoginKey] = useState('')

  function handleSubmit() {
    console.log('submit')
    console.log(username)
    console.log(password)
    console.log(key)
  }

  return (
    <Box>
      <Typography align="center" variant="h5">Register</Typography>
      <TextField
        margin="normal"
        required
        fullWidth
        label="Username"
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        label="Password"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        label="Key"
        type="password"
        onChange={(e) => setLoginKey(e.target.value)}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        color="primary"
        sx={{ mt: 2 }}
        onClick={handleSubmit}
      >
        Create Account
      </Button>
      <Link 
        href="/login" 
        sx={{ mt: 2, display: 'block', textAlign: 'center' }}
        >
        Login
      </Link>
    </Box>
  );
}