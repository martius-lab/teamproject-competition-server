import { Download } from "@mui/icons-material";
import { Box, Button, Divider, Grid, Paper, Stack, TextField, ThemeProvider, Typography, createTheme } from "@mui/material";
import { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { DashboardPaper } from "~/components/DashboardContent";
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

  var gameEnd = 'undefined'
  console.log(game.end_state)
  switch (game.end_state) {
    case 0:
      gameEnd = 'Win'
      break
    case 1:
      gameEnd = 'Draw'
      break
    case 2:
      gameEnd = 'Disconnect'
      break
  }

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
        <Grid container justifyContent={'center'} spacing={{xs: 0, md:2}} columnSpacing={{xs: 0, md:3}}>
          <Grid item xs={12} md={4} lg={5}>
            <Typography variant="h5" color={'primary.main'} padding={2} sx={{textAlign: {xs: "center", md:"right"}}}> {game.participants[0].name} </Typography>
          </Grid>
          <Grid item xs={12} md={1} lg={1}>
            <Typography 
              variant="h5" 
              align="center" 
              border={1} 
              borderTop={{xs: 1, md: 0}} 
              borderBottom={{xs: 1, md: 0}}
              borderLeft={{xs: 0, md: 1}}
              borderRight={{xs: 0, md: 1}}
              padding={2} 
              borderColor={'primary.main'} 
              color={'primary.main'}>
              {game.participants[0].score}  -  {game.participants[1].score}
            </Typography>
          </Grid>
          <Divider orientation="vertical" variant="fullWidth" />
          <Grid item xs={12} md={4} lg={5}>
            <Typography variant="h5" color={'primary.main'} padding={2} sx={{textAlign: {xs: "center", md:"left"}}}> {game.participants[1].name} </Typography>
          </Grid>
        </Grid>
        <Typography variant="h5"> {
        } </Typography>
      </Paper>
      <Grid container marginTop={1} spacing={3}>
        <Grid item xs={12} md={6}>
          <DashboardPaper>
            <Typography variant="h5" marginBottom={2}> Game Information </Typography>
            <Typography variant="body1"> Time Stamp: {game.start_time} </Typography>
            <Typography variant="body1"> Game End: {gameEnd} </Typography>
            {game.participants.map( (participant, i) => {
              if (participant.winner) return <Typography variant="body1"> Winner: {participant.name} </Typography>
              return null
            })}
            {game.participants.map( (participant, i) => {
              if (participant.disconnected) return <Typography variant="body1"> Winner: {participant.name} </Typography>
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