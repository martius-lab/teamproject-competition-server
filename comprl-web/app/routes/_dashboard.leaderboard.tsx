import { Typography, Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Paper } from "@mui/material";
import { LoaderFunctionArgs } from "@remix-run/node";
import { authenticator } from "~/services/auth.server";
import { getSession } from "~/services/session.server";
import { useLoaderData } from "@remix-run/react";
import { getRankedUsers } from "~/db/sqlite.data";

export async function loader({ request, params }: LoaderFunctionArgs) {
  const user = await authenticator.isAuthenticated(request, {
    failureRedirect: "/login",
  });

  const session = await getSession(request.headers.get("Cookie"));

  if (params.name !== user.name) {

    session.flash("popup", { message: "You don't have permission to access that page", severity: "error" });
  }

  const users = await getRankedUsers();
  return {
    users: users, loggedInUsername: user.name
  };


}

export default function Leaderboard() {
  const { users } = useLoaderData<typeof loader>();
  const { loggedInUsername } = useLoaderData<typeof loader>();
  return (
    <div>
      <Typography variant="h1">Leaderboard:</Typography>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Ranking</TableCell>
              <TableCell align="left">User</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user, index) => (
              <TableRow
                key={index}
                sx={{
                  '&:last-child td, &:last-child th': { border: 0 },
                  backgroundColor: user.username === loggedInUsername ? 'lightblue' : 'inherit'
                }}
              >
                <TableCell component="th" scope="index">
                  {index + 1}
                </TableCell>
                <TableCell align="left">{user.username}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}