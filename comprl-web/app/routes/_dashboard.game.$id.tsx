import { Download, EmojiEvents, WifiOff } from "@mui/icons-material";
import { Box, Button, Chip, Divider, Grid, Paper, Stack, TextField, ThemeProvider, Typography, colors, createTheme } from "@mui/material";
import { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { DashboardPaper, EndStateChip } from "~/components/DashboardContent";
import { getGame, getUsername } from "~/db/sqlite.data";
import { themeOptions } from "~/style/theme";

export async function loader({ request, params }: LoaderFunctionArgs) {
  const game_id = params.id
  const game = await getGame(game_id)

  return { id: game_id, game: game };
}


export default function Game() {
  const { id, game } = useLoaderData<typeof loader>();

  if (!game) { return (<Typography> No game with id {id} could be found.  </Typography>) }
  const theme = createTheme(themeOptions);


  const onDownload = () => {
    const link = document.createElement("a");
    // TODO: Download the correct files
    link.download = `download.txt`;
    link.href = "./download.txt";
    link.click();
  };

  return (
    <ThemeProvider theme={theme}>
      <Paper variant="outlined" sx={{ bgcolor: 'primary.light', borderColor: 'primary.main' }} >
        <Grid container justifyContent={'center'} spacing={{ xs: 0, md: 2 }} columnSpacing={{ xs: 0, md: 3 }}>
          <Grid item xs={12} md={4} lg={5}>
            <Stack direction={{ xs: "row", md: "row-reverse" }} alignItems="center" gap={1} justifyContent={{ xs: "center", md: "flex-start" }}>
              <Typography variant="h5" color={'primary.main'} padding={2}> {game.participants[0].name} </Typography>
              {game.participants[0].winner ? <EmojiEvents sx={{ color: colors.yellow[700] }} /> : null}
              {game.participants[0].disconnected ? <WifiOff sx={{ color: colors.red[700] }} /> : null}
            </Stack>
          </Grid>
          <Grid item xs={12} md={1} lg={1}>
            <Typography
              variant="h5"
              align="center"
              border={1}
              borderTop={{ xs: 1, md: 0 }}
              borderBottom={{ xs: 1, md: 0 }}
              borderLeft={{ xs: 0, md: 1 }}
              borderRight={{ xs: 0, md: 1 }}
              padding={2}
              borderColor={'primary.main'}
              color={'primary.main'}>
              {game.participants[0].score}  -  {game.participants[1].score}
            </Typography>
          </Grid>
          <Divider orientation="vertical" variant="fullWidth" />
          <Grid item xs={12} md={4} lg={5}>
            <Stack direction="row" alignItems="center" gap={1} justifyContent={{ xs: "center", md: "flex-start" }}>
              <Typography variant="h5" color={'primary.main'} padding={2}> {game.participants[1].name} </Typography>
              {game.participants[1].winner ? <EmojiEvents sx={{ color: colors.yellow[700] }} /> : null}
              {game.participants[1].disconnected ? <WifiOff sx={{ color: colors.red[700] }} /> : null}
            </Stack>
          </Grid>
        </Grid>
        <Typography variant="h5"> {
        } </Typography>
      </Paper>
      <Grid container marginTop={1} spacing={3}>
        <Grid item xs={12} md={6}>
          <DashboardPaper>
            <Typography variant="h5" marginBottom={2}> Game Information </Typography>
            <Stack direction="row" justifyContent={'flex-start'} alignItems={'center'}>
              <Typography variant="body1"> Game End: </Typography>
              <EndStateChip state={game.end_state} />
            </Stack>
            <Typography variant="body1"> Time Stamp: {game.start_time} </Typography>
            {game.participants.map((participant, i) => {
              if (participant.winner) return <Typography variant="body1"> Winner: {participant.name} </Typography>
              return null
            })}
            {game.participants.map((participant, i) => {
              if (participant.disconnected) return <Typography variant="body1"> Disconnected Player: {participant.name} </Typography>
              return null
            })}
          </DashboardPaper>
        </Grid>
        <Grid item xs={12} md={6}>
          <DashboardPaper>
            <Typography variant="h5" marginBottom={2}> Download Actions </Typography>
            <Button onClick={onDownload} variant="contained" color="primary">
              <Download />
              Download
            </Button>
          </DashboardPaper>
        </Grid>
      </Grid>
    </ThemeProvider >
  );
}