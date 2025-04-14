import React from 'react'
import ReactDOM from 'react-dom/client'
import { ClerkProvider } from '@clerk/clerk-react'
import { SupabaseProvider } from './contexts/SupabaseContext'
import { ApiProvider } from './contexts/ApiContext'
import App from './App'
import './index.css'

// Get Clerk publishable key from environment variables
const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!clerkPubKey) {
  console.error('Missing Clerk publishable key')
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={clerkPubKey}>
      <SupabaseProvider>
        <ApiProvider>
          <App />
        </ApiProvider>
      </SupabaseProvider>
    </ClerkProvider>
  </React.StrictMode>,
)
