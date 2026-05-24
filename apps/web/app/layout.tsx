import type { ReactNode } from 'react'

export const metadata = {
  title: 'SovereignBharat',
  description: "India's sovereign cloud and AI-native infrastructure platform.",
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
