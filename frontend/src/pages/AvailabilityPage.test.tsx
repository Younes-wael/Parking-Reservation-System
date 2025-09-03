import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import AvailabilityPage from './AvailabilityPage'
import { describe, it } from 'vitest'
import '@testing-library/jest-dom'

describe('AvailabilityPage', () => {
  it('renders heading', () => {
    const qc = new QueryClient()
    render(
      <QueryClientProvider client={qc}>
        <BrowserRouter>
          <AvailabilityPage />
        </BrowserRouter>
      </QueryClientProvider>
    )
    expect(screen.getByText(/Check Availability/i)).toBeInTheDocument()
  })
})
