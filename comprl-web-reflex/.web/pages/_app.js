/** @jsxImportSource @emotion/react */

import '$/styles/styles.css'

import RadixThemesColorModeProvider from "$/components/reflex/radix_themes_color_mode_provider.js"
import { Theme as RadixThemesTheme } from "@radix-ui/themes"
import theme from "$/utils/theme.js"
import { Fragment } from "react"


import { EventLoopProvider, StateProvider, defaultColorMode } from "$/utils/context.js";
import { ThemeProvider } from 'next-themes'
import * as next_link from "next/link";
import * as emotion_react from "@emotion/react";
import * as React from "react";
import * as radix_ui_themes from "@radix-ui/themes";
import * as utils_context from "$/utils/context";
import * as utils_state from "$/utils/state";


function AppWrap({children}) {


  return (
    <RadixThemesColorModeProvider>

<RadixThemesTheme accentColor={"teal"} css={{...theme.styles.global[':root'], ...theme.styles.global.body}} hasBackground={true}>

<Fragment>

{children}
</Fragment>
</RadixThemesTheme>
</RadixThemesColorModeProvider>
  )
}

export default function MyApp({ Component, pageProps }) {
  React.useEffect(() => {
    // Make contexts and state objects available globally for dynamic eval'd components
    let windowImports = {
      "next/link": next_link,
      "@emotion/react": emotion_react,
      "react": React,
      "@radix-ui/themes": radix_ui_themes,
      "$/utils/context": utils_context,
      "$/utils/state": utils_state,
    };
    window["__reflex"] = windowImports;
  }, []);
  return (
    <ThemeProvider defaultTheme={ defaultColorMode } attribute="class">
      <AppWrap>
        <StateProvider>
          <EventLoopProvider>
            <Component {...pageProps} />
          </EventLoopProvider>
        </StateProvider>
      </AppWrap>
    </ThemeProvider>
  );
}

