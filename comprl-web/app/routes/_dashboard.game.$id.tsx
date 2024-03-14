import { Download } from "@mui/icons-material";
import { Box, Button, Divider, Grid, Paper, Stack, TextField, ThemeProvider, Typography, createTheme } from "@mui/material";
import { LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { DashboardPaper } from "~/components/DashboardContent";
import { getGame, getUserName } from "~/db/sqlite.data";
import { themeOptions } from "~/style/theme";

export async function loader({ request, params }: LoaderFunctionArgs) {
  const game_id = params.id
  const game = await getGame(game_id)

  if (!game) { return { id: game_id, game: null, username1: null, username2: null } }

  const username1 = await getUserName(game.user1)
  const username2 = await getUserName(game.user2)

  return { id: game_id, game: game, username1: username1, username2: username2 };
}


export default function Game() {
  const { id, game, username1, username2 } = useLoaderData<typeof loader>();

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
            <Typography variant="h5" color={'primary.main'} padding={2} sx={{textAlign: {xs: "center", md:"right"}}}> {username1} </Typography>
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
              {game.score1}  -  {game.score2}
            </Typography>
          </Grid>
          <Divider orientation="vertical" variant="fullWidth" />
          <Grid item xs={12} md={4} lg={5}>
            <Typography variant="h5" color={'primary.main'} padding={2} sx={{textAlign: {xs: "center", md:"left"}}}> {username2} </Typography>
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
            {game.winner && <Typography variant="body1"> Winner: {game.winner==game.user1? username1 : username2} </Typography>}
            {game.disconnected && <Typography variant="body1"> Disconnected Player: {game.disconnected==game.user1? username1 : username2} </Typography>}
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