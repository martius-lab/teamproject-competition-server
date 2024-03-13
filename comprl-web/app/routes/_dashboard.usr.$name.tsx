import { Typography, Grid, IconButton } from "@mui/material";
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { LoaderFunctionArgs, redirect } from "@remix-run/node";
import { authenticator } from "~/services/auth.server";
import { commitSession, getSession } from "~/services/session.server";
import { useLoaderData } from "@remix-run/react";
import { getStatistics } from "~/db/sqlite.data";
import { DashboardsStatistic, DashboardPaper } from '~/components/DashboardContent';
import React from "react";



export async function loader({ request, params }: LoaderFunctionArgs) {
  const user = await authenticator.isAuthenticated(request, {
    failureRedirect: "/login",
  });

  const session = await getSession(request.headers.get("Cookie"));

  if (params.name !== user.name) {

    session.flash("popup", { message: "You don't have permission to access that page", severity: "error" });

    return redirect(`/usr/${user.name}`, {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    });
  }

  const games = await getStatistics(user.id)

  if (!user.token) {
    return { token: "no token exists", username: user.name, games: games };
  }


  return { token: user.token, username: user.name, games: games};
}

export default function UserDashboard() {
  const { token, username, games } = useLoaderData<typeof loader>();
  const [selected, setSelected] = React.useState(false);
  return (
    <div>
      <Grid container spacing={3} alignItems="stretch">
        <Grid item xs={12} md={6}>
          <DashboardPaper>
            <Typography variant="h5" > Username </Typography> 
            <Typography>{username}</Typography>
          </DashboardPaper> 
        </Grid>
        <Grid item xs={12} md={6}>
          <DashboardPaper> 
            <Typography variant="h5" > Token 
              <IconButton onClick={() => { setSelected(!selected); }}>
              {selected ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </Typography>
            <Typography>{selected ? token : "*************" }</Typography>
          </DashboardPaper>
        </Grid>
        <Grid item xs={12}>
          <DashboardPaper>
          <Typography variant="h5"> Game Statistics </Typography>
            <Grid container spacing={8} padding={5}>
              <Grid item xs={12} md={6} lg={3}><DashboardsStatistic value={games.playedGames.toString()} description="games played" /></Grid>
              <Grid item xs={12} md={6} lg={3}><DashboardsStatistic value={games.wonGames.toString()} description="games won" /></Grid>
              <Grid item xs={12} md={6} lg={3}><DashboardsStatistic value={Math.round((games.wonGames/games.playedGames)*100) + "%"} description="win rate" /></Grid>
              <Grid item xs={12} md={6} lg={3}><DashboardsStatistic value={games.disconnectedGames.toString()} description="disconnects" /></Grid>
            </Grid>
          </DashboardPaper>
        </Grid>
      </Grid>
    </div>
  );
}