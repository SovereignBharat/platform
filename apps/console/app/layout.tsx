import type { ReactNode } from 'react'

export const metadata = {
  title: 'SovereignBharat Console',
  description: 'Control plane dashboard',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
