// src/theme/index.ts
import { extendTheme, ThemeConfig } from '@chakra-ui/react';

/** 1. Light mode as default */
const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: false,
};

/** 2. Brand colors (optional) */
const colors = {
  brand: {
    50:  '#e3f2ff',
    100: '#b3d4ff',
    200: '#81b7ff',
    300: '#4e9aff',
    400: '#1d7dff',
    500: '#0364e6',   // primary
    600: '#004db4',
    700: '#003782',
    800: '#00234f',
    900: '#000e1f',
  },
};

export const theme = extendTheme({ config, colors });
