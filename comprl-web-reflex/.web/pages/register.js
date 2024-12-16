/** @jsxImportSource @emotion/react */


import { ErrorBoundary } from "react-error-boundary"
import { Fragment, useCallback, useContext, useEffect, useRef, useState } from "react"
import { ColorModeContext, EventLoopContext, StateContexts } from "$/utils/context"
import { Event, getBackendURL, getRefValue, getRefValues, isTrue, refs } from "$/utils/state"
import { jsx, keyframes } from "@emotion/react"
import { TriangleAlertIcon as LucideTriangleAlertIcon, WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { toast, Toaster } from "sonner"
import env from "$/env.json"
import { Button as RadixThemesButton, Callout as RadixThemesCallout, Card as RadixThemesCard, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Link as RadixThemesLink, Separator as RadixThemesSeparator, Text as RadixThemesText, TextField as RadixThemesTextField } from "@radix-ui/themes"
import NextLink from "next/link"
import { Root as RadixFormRoot } from "@radix-ui/react-form"
import NextHead from "next/head"



export function Div_bd4c022a8f796682aa6392e9d4c102e9 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <div css={({ ["position"] : "fixed", ["width"] : "100vw", ["height"] : "0" })} title={("Connection Error: "+((connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''))}>

<Fragment_9017984ada32ffa55f5d2870ebd3c887/>
</div>
  )
}

export function Errorboundary_eb61a48061f392af64889773d36fb812 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_error_0f5dbf674521530422d73a7946faf6d4 = useCallback(((_error, _info) => (addEvents([(Event("reflex___state____state.reflex___state____frontend_event_exception_state.handle_frontend_exception", ({ ["stack"] : _error["stack"], ["component_stack"] : _info["componentStack"] }), ({  })))], [_error, _info], ({  })))), [addEvents, Event])


  return (
    <ErrorBoundary fallbackRender={((event_args) => (jsx("div", ({ ["css"] : ({ ["height"] : "100%", ["width"] : "100%", ["position"] : "absolute", ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center" }) }), (jsx("div", ({ ["css"] : ({ ["display"] : "flex", ["flexDirection"] : "column", ["gap"] : "1rem" }) }), (jsx("div", ({ ["css"] : ({ ["display"] : "flex", ["flexDirection"] : "column", ["gap"] : "1rem", ["maxWidth"] : "50ch", ["border"] : "1px solid #888888", ["borderRadius"] : "0.25rem", ["padding"] : "1rem" }) }), (jsx("h2", ({ ["css"] : ({ ["fontSize"] : "1.25rem", ["fontWeight"] : "bold" }) }), (jsx(Fragment, ({  }), "An error occurred while rendering this page.")))), (jsx("p", ({ ["css"] : ({ ["opacity"] : "0.75" }) }), (jsx(Fragment, ({  }), "This is an error with the application itself.")))), (jsx("details", ({  }), (jsx("summary", ({ ["css"] : ({ ["padding"] : "0.5rem" }) }), (jsx(Fragment, ({  }), "Error message")))), (jsx("div", ({ ["css"] : ({ ["width"] : "100%", ["maxHeight"] : "50vh", ["overflow"] : "auto", ["background"] : "#000", ["color"] : "#fff", ["borderRadius"] : "0.25rem" }) }), (jsx("div", ({ ["css"] : ({ ["padding"] : "0.5rem", ["width"] : "fit-content" }) }), (jsx("pre", ({  }), (jsx(Fragment, ({  }), event_args.error.stack)))))))), (jsx("button", ({ ["css"] : ({ ["padding"] : "0.35rem 0.75rem", ["margin"] : "0.5rem", ["background"] : "#fff", ["color"] : "#000", ["border"] : "1px solid #000", ["borderRadius"] : "0.25rem", ["fontWeight"] : "bold" }), ["onClick"] : ((...args) => (addEvents([(Event("_call_function", ({ ["function"] : (() => (navigator["clipboard"]["writeText"](event_args.error.stack))) }), ({  })))], args, ({  })))) }), (jsx(Fragment, ({  }), "Copy")))))))), (jsx("hr", ({ ["css"] : ({ ["borderColor"] : "currentColor", ["opacity"] : "0.25" }) }))), (jsx("a", ({ ["href"] : "https://reflex.dev" }), (jsx("div", ({ ["css"] : ({ ["display"] : "flex", ["alignItems"] : "baseline", ["justifyContent"] : "center", ["fontFamily"] : "monospace", ["--default-font-family"] : "monospace", ["gap"] : "0.5rem" }) }), (jsx(Fragment, ({  }), "Built with ")), (jsx("svg", ({ ["css"] : ({ ["viewBox"] : "0 0 56 12", ["fill"] : "currentColor" }), ["height"] : "12", ["width"] : "56", ["xmlns"] : "http://www.w3.org/2000/svg" }), (jsx("path", ({ ["d"] : "M0 11.5999V0.399902H8.96V4.8799H6.72V2.6399H2.24V4.8799H6.72V7.1199H2.24V11.5999H0ZM6.72 11.5999V7.1199H8.96V11.5999H6.72Z" }))), (jsx("path", ({ ["d"] : "M11.2 11.5999V0.399902H17.92V2.6399H13.44V4.8799H17.92V7.1199H13.44V9.3599H17.92V11.5999H11.2Z" }))), (jsx("path", ({ ["d"] : "M20.16 11.5999V0.399902H26.88V2.6399H22.4V4.8799H26.88V7.1199H22.4V11.5999H20.16Z" }))), (jsx("path", ({ ["d"] : "M29.12 11.5999V0.399902H31.36V9.3599H35.84V11.5999H29.12Z" }))), (jsx("path", ({ ["d"] : "M38.08 11.5999V0.399902H44.8V2.6399H40.32V4.8799H44.8V7.1199H40.32V9.3599H44.8V11.5999H38.08Z" }))), (jsx("path", ({ ["d"] : "M47.04 4.8799V0.399902H49.28V4.8799H47.04ZM53.76 4.8799V0.399902H56V4.8799H53.76ZM49.28 7.1199V4.8799H53.76V7.1199H49.28ZM47.04 11.5999V7.1199H49.28V11.5999H47.04ZM53.76 11.5999V7.1199H56V11.5999H53.76Z" }))))))))))))))} onError={on_error_0f5dbf674521530422d73a7946faf6d4}>

<Fragment>

<Div_bd4c022a8f796682aa6392e9d4c102e9/>
<Toaster_6e6ebf8d7ce589d59b7d382fb7576edf/>
</Fragment>
<Fragment>

<RadixThemesFlex align={"center"} className={"rx-Stack"} css={({ ["paddingTop"] : "10%" })} direction={"column"} gap={"2"}>

<RadixThemesHeading css={({ ["fontSize"] : "2em" })}>

{"RL Competition"}
</RadixThemesHeading>
<Fragment>

<RadixThemesFlex align={"start"} className={"rx-Stack"} css={({ ["flexDirection"] : "row" })} gap={"3"}>

<RadixThemesLink asChild={true} css={({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })}>

<NextLink href={"/"} passHref={true}>

{"Home"}
</NextLink>
</RadixThemesLink>
<RadixThemesLink asChild={true} css={({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })}>

<NextLink href={"/dashboard"} passHref={true}>

{"Dashboard"}
</NextLink>
</RadixThemesLink>
<RadixThemesLink asChild={true} css={({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })}>

<NextLink href={"/leaderboard"} passHref={true}>

{"Leaderboard"}
</NextLink>
</RadixThemesLink>
<Fragment_bb982cb70f20da9ebf0dbffef4a6beb8/>
</RadixThemesFlex>
<RadixThemesSeparator size={"4"}/>
</Fragment>
<RadixThemesFlex css={({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["paddingTop"] : "10vh" })}>

<Fragment_c953cbfde1a6876827ee4c399174fd8e/>
</RadixThemesFlex>
</RadixThemesFlex>
</Fragment>
<NextHead>

<title>

{"Register"}
</title>
<meta content={"favicon.ico"} property={"og:image"}/>
</NextHead>
</ErrorBoundary>
  )
}

export function Fragment_c953cbfde1a6876827ee4c399174fd8e () {
  const reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state__comprl_web___reflex_local_auth___registration____registration_state = useContext(StateContexts.reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state__comprl_web___reflex_local_auth___registration____registration_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  const ref_key = useRef(null); refs["ref_key"] = ref_key;
  const ref_username = useRef(null); refs["ref_username"] = ref_username;
  const ref_password = useRef(null); refs["ref_password"] = ref_password;
  const ref_confirm_password = useRef(null); refs["ref_confirm_password"] = ref_confirm_password;


  
    const handleSubmit_00f8a1762ffc57b4cd369aab3827b8d2 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({ ["password"] : getRefValue(refs["ref_password"]), ["username"] : getRefValue(refs["ref_username"]), ["confirm_password"] : getRefValue(refs["ref_confirm_password"]), ["key"] : getRefValue(refs["ref_key"]) })};

        (((...args) => (addEvents([(Event("reflex___state____state.comprl_web___reflex_local_auth___local_auth____local_auth_state.comprl_web___reflex_local_auth___registration____registration_state.handle_registration", ({ ["form_data"] : form_data }), ({  })))], args, ({  }))))());

        if (false) {
            $form.reset()
        }
    })
    

  return (
    <Fragment>

{isTrue(reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state__comprl_web___reflex_local_auth___registration____registration_state.success) ? (
  <Fragment>

<RadixThemesFlex align={"start"} className={"rx-Stack"} direction={"column"} gap={"3"}>

<RadixThemesText as={"p"}>

{"Registration successful!"}
</RadixThemesText>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment>

<RadixThemesCard>

<RadixFormRoot className={"Root "} css={({ ["width"] : "100%" })} onSubmit={handleSubmit_00f8a1762ffc57b4cd369aab3827b8d2}>

<RadixThemesFlex align={"start"} className={"rx-Stack"} css={({ ["minWidth"] : "50vw" })} direction={"column"} gap={"3"}>

<RadixThemesHeading size={"7"}>

{"Create an account"}
</RadixThemesHeading>
<Fragment>

{isTrue(!((reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state__comprl_web___reflex_local_auth___registration____registration_state.error_message === ""))) ? (
  <Fragment>

<RadixThemesCallout.Root color={"red"} css={({ ["icon"] : "triangle_alert", ["width"] : "100%" })} role={"alert"}>

<RadixThemesCallout.Icon>

<LucideTriangleAlertIcon css={({ ["color"] : "var(--current-color)" })}/>
</RadixThemesCallout.Icon>
<RadixThemesCallout.Text>

{reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state__comprl_web___reflex_local_auth___registration____registration_state.error_message}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
<RadixThemesText as={"p"}>

{"Registration Key"}
</RadixThemesText>
<RadixThemesTextField.Root css={({ ["width"] : "100%" })} id={"key"} name={"key"} placeholder={"Key"} ref={ref_key}/>
<RadixThemesText as={"p"}>

{"Username"}
</RadixThemesText>
<RadixThemesTextField.Root css={({ ["width"] : "100%" })} id={"username"} name={"username"} placeholder={"Username"} ref={ref_username}/>
<RadixThemesText as={"p"}>

{"Password"}
</RadixThemesText>
<RadixThemesTextField.Root css={({ ["width"] : "100%" })} id={"password"} name={"password"} placeholder={"Password"} ref={ref_password} type={"password"}/>
<RadixThemesText as={"p"}>

{"Repeat Password"}
</RadixThemesText>
<RadixThemesTextField.Root css={({ ["width"] : "100%" })} id={"confirm_password"} name={"confirm_password"} placeholder={"Confirm Password"} ref={ref_confirm_password} type={"password"}/>
<RadixThemesButton css={({ ["width"] : "100%" })}>

{"Sign up"}
</RadixThemesButton>
<RadixThemesFlex css={({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100%" })}>

<RadixThemesLink css={({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })} onClick={((...args) => (addEvents([(Event("_redirect", ({ ["path"] : "/login", ["external"] : false, ["replace"] : false }), ({  })))], args, ({  }))))}>

{"Login"}
</RadixThemesLink>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixFormRoot>
</RadixThemesCard>
</Fragment>
)}
</Fragment>
  )
}

export function Fragment_9017984ada32ffa55f5d2870ebd3c887 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <Fragment>

{isTrue((connectErrors.length > 0)) ? (
  <Fragment>

<LucideWifiOffIcon css={({ ["color"] : "crimson", ["zIndex"] : 9999, ["position"] : "fixed", ["bottom"] : "33px", ["right"] : "33px", ["animation"] : (pulse+" 1s infinite") })} size={32}/>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

const pulse = keyframes`
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
`


export function Fragment_bb982cb70f20da9ebf0dbffef4a6beb8 () {
  const reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state = useContext(StateContexts.reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <Fragment>

{isTrue(reflex___state____state__comprl_web___reflex_local_auth___local_auth____local_auth_state.is_authenticated) ? (
  <Fragment>

<RadixThemesLink asChild={true} css={({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })} onClick={((...args) => (addEvents([(Event("reflex___state____state.comprl_web___reflex_local_auth___local_auth____local_auth_state.do_logout", ({  }), ({  })))], args, ({  }))))}>

<NextLink href={"/"} passHref={true}>

{"Logout"}
</NextLink>
</RadixThemesLink>
</Fragment>
) : (
  <Fragment>

<RadixThemesLink asChild={true} css={({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })}>

<NextLink href={"/login"} passHref={true}>

{"Login"}
</NextLink>
</RadixThemesLink>
<RadixThemesLink asChild={true} css={({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })}>

<NextLink href={"/register"} passHref={true}>

{"Register"}
</NextLink>
</RadixThemesLink>
</Fragment>
)}
</Fragment>
  )
}

export function Toaster_6e6ebf8d7ce589d59b7d382fb7576edf () {
  const { resolvedColorMode } = useContext(ColorModeContext)


  refs['__toast'] = toast
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  const toast_props = ({ ["description"] : ("Check if server is reachable at "+getBackendURL(env.EVENT).href), ["closeButton"] : true, ["duration"] : 120000, ["id"] : "websocket-error" });
  const [userDismissed, setUserDismissed] = useState(false);
  (useEffect(
() => {
    if ((connectErrors.length >= 2)) {
        if (!userDismissed) {
            toast.error(
                `Cannot connect to server: ${((connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : '')}.`,
                {...toast_props, onDismiss: () => setUserDismissed(true)},
            )
        }
    } else {
        toast.dismiss("websocket-error");
        setUserDismissed(false);  // after reconnection reset dismissed state
    }
}
, [connectErrors]))

  return (
    <Toaster closeButton={false} expand={true} position={"bottom-right"} richColors={true} theme={resolvedColorMode}/>
  )
}

export default function Component() {

  return (
    <Errorboundary_eb61a48061f392af64889773d36fb812/>
  )
}