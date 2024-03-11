import { Paper, Typography , ThemeProvider} from '@mui/material'
import { themeOptions } from "~/style/theme";

interface DashboardContentProps {
    caption: string;
    children: React.ReactNode;
}

function DashboardContent({ caption, children}: DashboardContentProps) {
    return (

        <Paper elevation={5} sx={{p:4, borderRadius:6, bgcolor: '#d3e0eb' }}>
            <Typography variant="h5" align="left">{caption}</Typography>
            {children}
        </Paper>

    )
}

export default DashboardContent