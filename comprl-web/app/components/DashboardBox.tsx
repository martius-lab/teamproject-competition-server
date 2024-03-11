import { themeOptions } from "~/style/theme";
import { Typography, Box, Stack, ThemeProvider } from "@mui/material";

export default function DashboardBox({title, value}: {title: string, value: string}) {

return (
<ThemeProvider theme={themeOptions}>
    <Box
      my={6}
      display="flex"
      gap={2}
      p={3}
      borderRadius={2}
      sx={{
        border: '2px solid primary.main',
        bgcolor: 'primary.light'
      }}
    >
        <Stack>
            <Typography variant="body1" color='primary.main'>{title}</Typography>
            <Typography variant="h4" color='primary.main'>{value}</Typography>
        </Stack>
    </Box>
    </ThemeProvider>
)}