import { Container, Paper } from "@mui/material";
import { Outlet } from "@remix-run/react";

export default function AuthLayout() {
    return (
        <Container maxWidth="xs" sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh'}}>
            <Paper square={false} elevation={16} sx={{ padding: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%'}}>
                <Outlet />
            </Paper>
        </Container>
    );
}