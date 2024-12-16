import { Alert, Snackbar } from '@mui/material';
import { useState } from 'react';

export default function AutoHideSnackbar({ message, severity }: { message: string, severity: "error" | "warning" | "info" | "success" }) {
    const [open, setOpen] = useState(true);

    const handleClose = (event: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway') {
            return;
        }

        setOpen(false);
    };

    return (
        <Snackbar open={open} autoHideDuration={4000} onClose={handleClose} anchorOrigin={{horizontal: 'center', vertical:'bottom'}}>
            <Alert
                onClose={handleClose}
                severity={severity}
                variant="filled"
                sx={{ width: '100%' }}
            >
                {message}
            </Alert>
        </Snackbar>
    );
}