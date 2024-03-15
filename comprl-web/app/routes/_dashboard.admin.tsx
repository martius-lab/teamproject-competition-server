import * as React from 'react';
import { Box, Typography, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Button, AlertProps} from "@mui/material";
import { DataGrid, GridColDef, GridRowModel,} from "@mui/x-data-grid";
import { ActionFunctionArgs, LoaderFunctionArgs, redirect } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { authenticator } from "~/services/auth.server";
import { commitSession, getSession } from "~/services/session.server";
import { editUser, getAllUsers } from "~/db/sqlite.data";

export async function loader({ request, params }: LoaderFunctionArgs) {
  const user = await authenticator.isAuthenticated(request, {
    failureRedirect: "/login",
  });

  const session = await getSession(request.headers.get("Cookie"));

  // TODO admin role check
  //if (params.role != "admin") {
  if (false) {

    session.flash("popup", { message: "You don't have permission to access that page", severity: "error" });

    return redirect(`/usr/${user.name}`, {
      headers: {
        "Set-Cookie": await commitSession(session),
      },
    });
  }

  const users = await getAllUsers();

  return { users: users };
}

const useFakeMutation = () => {
  return React.useCallback(
    (user) =>
      new Promise((resolve, reject) => {
        setTimeout(() => {
          if (user.name?.trim() === '') {
            reject();
          } else {
            resolve(user);
          }
        }, 200);
      }),
    [],
  );
};

export async function action({ request }: ActionFunctionArgs) {
  const body = await request.json(); // Parse JSON data from the request body
  if (body.row) {
    await editUser(body.id, body.username, body.password, body.role, body.token, body.mu, body.sigma);
  }
  // console.log('body:', body);
  return {}
}

const columns: GridColDef[] = [
  {
    field: 'id',
    headerName: 'user ID',
    //width: 70, 
    sortable: false,
    editable: false,
  },
  {
    field: 'username',
    headerName: 'Username',
    type: 'string',
    //width: 150,
    editable: true,
  },
  {
    field: 'password',
    headerName: 'Password',
    type: 'string',
    //width: 150,
    editable: true,
  },
  {
    field: 'role',
    headerName: 'Role',
    type: 'string', // TODO change to enum "admin" | "user" | "bot"
    //width: 70,
    editable: true,
  },
  {
    field: 'token',
    headerName: 'Token',
    //width: 160,
    editable: true,
  },
  {
    field: 'mu',
    headerName: 'Mu',
    type: 'number',
    //width: 110,
    editable: true,
  },
  {
    field: 'sigma',
    headerName: 'Sigma',
    type: 'number',
    //width: 110,
    editable: true,
  },
];

function createRow(id: number, username: string, password: string, role: string, token: string, mu: number, sigma: number) {
  return { id, username, password, role, token, mu, sigma };

}



export default function Admin() {
  const { users } = useLoaderData<typeof loader>();
  const rows = users.map((user) => createRow(user.user_id, user.username, user.password, user.role, user.token, user.mu, user.sigma));
  const noButtonRef = React.useRef<HTMLButtonElement>(null);
  const [promiseArguments, setPromiseArguments] = React.useState<any>(null);

  const processRowUpdate = React.useCallback(
    (newRow: GridRowModel, oldRow: GridRowModel) =>
      new Promise<GridRowModel>((resolve, reject) => {
        if (newRow == oldRow) {
          resolve(oldRow); // Nothing was changed
        } else {
          // Save the arguments to resolve or reject the promise later
          setPromiseArguments({ resolve, reject, newRow, oldRow });
        }
      }),
    [],
  );

  const handleNo = () => {
    const { oldRow, resolve } = promiseArguments;
    resolve(oldRow); // Resolve with the old row to not update the internal state
    setPromiseArguments(null);
  };

  const handleYes = async () => {
    const { newRow, oldRow, reject, resolve } = promiseArguments;
    // send the changes to the server
    try {
      const response = await fetch('', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'row': newRow}),
      });
      resolve(response);
      setPromiseArguments(null);
    } catch (error) {
      console.error('Error sending data:', error);
      reject(oldRow);
      setPromiseArguments(null);
    }
  };

  const handleEntered = () => {
    // The `autoFocus` is not used because, if used, the same Enter that saves
    // the cell triggers "No". Instead, we manually focus the "No" button once
    // the dialog is fully open.
    // noButtonRef.current?.focus();
  };

  const renderConfirmDialog = () => {
    if (!promiseArguments) {
      return null;
    }

    const { newRow, oldRow } = promiseArguments;

    return (
      <Dialog
        maxWidth="xs"
        TransitionProps={{ onEntered: handleEntered }}
        open={!!promiseArguments}
      >
        <DialogTitle>Are you sure?</DialogTitle>
        <DialogContent dividers>
          {`Pressing 'Yes' will apply the changes to the database.`}
        </DialogContent>
        <DialogActions>
          <Button ref={noButtonRef} onClick={handleNo}>
            No
          </Button>
          <Button onClick={handleYes}>Yes</Button>
        </DialogActions>
      </Dialog>
    );
  };


  return (
    <div>
      <Typography variant="h1">Admin</Typography>
      <Typography variant="h2">Users</Typography>
      <Box sx={{ height: 625, width: '100%' }}>
        {renderConfirmDialog()}
        <DataGrid
          rows={rows}
          columns={columns}
          initialState={{
            pagination: {
              paginationModel: {
                pageSize: 10,
              },
            },
          }}
          pageSizeOptions={[10, 20, 50, { label: 'All', value: -1 }]}
          disableRowSelectionOnClick
          editMode="row"
          processRowUpdate={processRowUpdate}
        />
      </Box>
    </div>
  )
}
