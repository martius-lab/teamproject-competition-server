import { Paper, Typography , ThemeProvider, createTheme, styled, Chip } from '@mui/material'
import { themeOptions } from "~/style/theme";

interface DashboardStatisticProps {
    value: string;
    description: string;
}

const theme = createTheme(themeOptions);

export function DashboardsStatistic({ value, description}: DashboardStatisticProps) {
    return (
        <ThemeProvider theme={theme}>
        <Paper variant="outlined" sx={{p:4, borderRadius:3, bgcolor: 'primary.light', paddingTop: theme.spacing(6), paddingBottom: theme.spacing(6), height: '100%' }}>
            <Typography variant="h3" align="center" color='primary.main'>{value}</Typography>
            <Typography variant="body1" align="center" color='primary.main'>{description}</Typography>
        </Paper>
        </ThemeProvider>
    )
}

export const DashboardPaper = styled(Paper)(() => ({
    padding: theme.spacing(5),
    borderRadius:4,
    height: '100%'
}));

export function EndStateChip({ state } : { state: number}) {
    switch (state) {
      case 0:
        return <Chip label="Finished" color="success" />;
      case 1:
        return <Chip label="Draw" color="info" />;
      case 2:
        return <Chip label="Disconnected" color="warning" />;
      default:
        return <Chip label="Error" color="primary" />;
    }
  }
