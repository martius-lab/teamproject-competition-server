import { AppBar, Box, Button, CssBaseline, Drawer, IconButton, List, ListItemButton, ListItemIcon, ListItemText, Toolbar, Typography } from '@mui/material';
import { AdminPanelSettingsOutlined, LogoutOutlined, ManageSearchOutlined, MenuRounded, SmartToyOutlined, LeaderboardOutlined } from '@mui/icons-material';
import { Outlet, useLoaderData } from '@remix-run/react';
import { useState } from 'react';
import { LoaderFunctionArgs, json } from '@remix-run/node';
import { commitSession, getSession } from '~/services/session.server';
import AutoHideSnackbar from '~/components/AutoHideSnackbar';

const drawerWidth = 240;

export async function loader({request}: LoaderFunctionArgs) {
  
  const session = await getSession(request.headers.get("Cookie"));
  const popup = session.get("popup");
  
  return json(
      {popup},
      {
          headers: {
              "Set-Cookie": await commitSession(session),
          }
      }
    );
}


export default function DashboardLayout() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);

  const handleDrawerClose = () => {
    setIsClosing(true);
    setMobileOpen(false);
  };

  const handleDrawerTransitionEnd = () => {
    setIsClosing(false);
  };

  const handleDrawerToggle = () => {
    if (!isClosing) {
      setMobileOpen(!mobileOpen);
    }
  };

  const drawerContent = (
    <Box>
      <Toolbar />
      <List>
        <ListItemButton sx={{ m: 1 }} href='/me'>
          <ListItemIcon>
            <SmartToyOutlined />
          </ListItemIcon>
          <ListItemText primary="Home" />
        </ListItemButton>
        <ListItemButton sx={{ m: 1 }} href='/leaderboard'>
          <ListItemIcon>
            <LeaderboardOutlined />
          </ListItemIcon>
          <ListItemText primary="Leaderboard" />
        </ListItemButton>
        <ListItemButton sx={{ m: 1 }} href='/games'>
          <ListItemIcon>
            <ManageSearchOutlined />
          </ListItemIcon>
          <ListItemText primary="Games" />
        </ListItemButton>
        <ListItemButton sx={{ m: 1 }} href='/admin'>
          <ListItemIcon>
            <AdminPanelSettingsOutlined />
          </ListItemIcon>
          <ListItemText primary="Admin" />
        </ListItemButton>
      </List>
    </Box>
  );

  const data = useLoaderData<typeof loader>()
  //console.log(data.popup)

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar
        position="fixed"
        color='transparent'
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          color: 'white',
          boxShadow: 'none',
          backdropFilter:"blur(20px)"
        }}
      >
        <Toolbar>
          <IconButton
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuRounded />
          </IconButton>
          <Typography color='primary' variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Dashboard
          </Typography>
          <Button startIcon={<LogoutOutlined />}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
        aria-label="mailbox folders"
      >
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onTransitionEnd={handleDrawerTransitionEnd}
          onClose={handleDrawerClose}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawerContent}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawerContent}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{ flexGrow: 1, p: 3, width: { sm: `calc(100% - ${drawerWidth}px)` } }}
      >
        <Toolbar />
        {data.popup && <AutoHideSnackbar message={data.popup.message} severity={data.popup.severity} />}
        <Outlet />
      </Box>
    </Box>
  );
}