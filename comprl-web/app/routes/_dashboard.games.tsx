import { EmojiEvents, Search, WifiOff } from "@mui/icons-material";
import { Box, Chip, Grid, IconButton, InputBase, Pagination, Paper, Stack, Table, TableBody, TableCell, TableContainer, TableHead, TablePagination, TableRow, Typography } from "@mui/material";
import { colors } from "@mui/material";
import { ActionFunctionArgs, redirect } from "@remix-run/node";
import { Link, useActionData } from "@remix-run/react";
import React from "react";
import { EndStateChip } from "~/components/DashboardContent";
import { searchGames } from "~/db/sqlite.data";
import { Game } from "~/db/types";

export async function action({ request }: ActionFunctionArgs) {

  const formData = await request.formData();
  const searchRequest = formData.get("search") as string;
  const searchResult = await searchGames(searchRequest);

  return { query: searchResult };
}

export default function Games() {

  const actionData = useActionData<typeof action>();
  const [page, setPage] = React.useState(1);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const handlePageChange = (event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };


  function renderParticipants(participants: [{ name: string, score: number, winner: boolean, disconnected: boolean }]) {
    return (
      <Stack direction="column" alignItems="flex-start" justifyContent="center">
        {participants.map((participant, idx) => (
          <Stack key={idx} direction="row" alignItems="center" gap={1}>
            <Typography variant="body1">{participant.name}</Typography>
            {participant.winner ? <EmojiEvents sx={{ color: colors.yellow[700] }} /> : null}
            {participant.disconnected ? <WifiOff sx={{ color: colors.red[700] }} /> : null}
          </Stack>
        ))}
      </Stack>
    )
  }

  return (
    <Box>
      <Grid container justifyContent={'center'}>
        <Paper
          component="form"
          method="POST"
          sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: '100%', maxWidth: 800 }}
        >
          <InputBase
            fullWidth
            sx={{ ml: 1, flex: 1 }}
            placeholder="Search Games"
            name="search"
          />
          <IconButton type="submit" sx={{ p: '10px' }} aria-label="search" >
            <Search />
          </IconButton>
        </Paper>
      </Grid>
      <Grid container justifyContent={'center'}>
        <TableContainer
          component={Paper}
          sx={{ width: '100%', maxWidth: 1000, mt: 2 }}
        >
          <Table sx={{ minWidth: 300 }} aria-label="simple table" >
            <TableHead>
              <TableRow>
                <TableCell align="left">ID</TableCell>
                <TableCell align="left">End-State</TableCell>
                <TableCell align="left">Participants</TableCell>
                <TableCell align="left">Time</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {actionData?.query.games
              .slice((page - 1) * rowsPerPage, (page - 1) * rowsPerPage + rowsPerPage)
              .map((game: Game) => (
                <TableRow
                  key={game.game_id}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 }, cursor: 'pointer' }}
                  hover
                  onClick={() => window.location.href = `/games/${game.game_id}`}
                >
                  <TableCell component="th" scope="row">{game.game_id}</TableCell>
                  <TableCell align="left">
                    <EndStateChip state={game.end_state} />
                  </TableCell>
                  <TableCell align="left">
                    {renderParticipants(game.participants)}
                  </TableCell>
                  <TableCell align="left">{game.start_time}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <Grid container justifyContent={'center'}>
            {actionData?.query.games&&<Pagination count={Math.ceil(actionData.query.games.length / rowsPerPage)} sx={{ m: 2 }} page={page} onChange={handlePageChange}/>}
          </Grid>
        </TableContainer>
      </Grid>
    </Box>
  );
}