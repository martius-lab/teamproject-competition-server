import { Paper, Typography } from '@mui/material'

interface DashboardContentProps {
    caption: string;
    children: React.ReactNode;
}

function DashboardContent({ caption, children}: DashboardContentProps) {
    return (
        <Paper sx={{p:4, borderRadius:6, boxShadow: 'rgba(145, 158, 171, 0.08) 0px 0px 2px 0px, rgba(145, 158, 171, 0.08) 0px 12px 24px -4px' }}>
            <Typography variant="h5" align="left">{caption}</Typography>
            {children}
        </Paper>
    )
}

export default DashboardContent