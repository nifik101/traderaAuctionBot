import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ScriptManagement from '../pages/ScriptManagement';

// Mock the API context
jest.mock('../contexts/ApiContext', () => ({
  useApi: () => ({
    isLoading: false,
    scripts: {
      getAll: jest.fn().mockResolvedValue([
        {
          id: 1,
          name: 'Test Script',
          search_parameters: {
            keywords: 'test keywords',
            categoryId: 123,
            minPrice: 100,
            maxPrice: 1000
          },
          is_active: true,
          schedule: '0 * * * *',
          last_run_at: '2025-04-14T10:00:00Z'
        }
      ]),
      toggle: jest.fn().mockResolvedValue({}),
      update: jest.fn().mockResolvedValue({}),
      create: jest.fn().mockResolvedValue({}),
      delete: jest.fn().mockResolvedValue(true)
    }
  }),
}));

describe('ScriptManagement Component', () => {
  test('renders script management page with script list', async () => {
    render(<ScriptManagement />);
    
    // Check for page title
    expect(screen.getByText(/Script Management/i)).toBeInTheDocument();
    
    // Check for create button
    expect(screen.getByText(/Create New Script/i)).toBeInTheDocument();
    
    // Check for table headers
    expect(screen.getByText(/Name/i)).toBeInTheDocument();
    expect(screen.getByText(/Keywords/i)).toBeInTheDocument();
    expect(screen.getByText(/Schedule/i)).toBeInTheDocument();
    expect(screen.getByText(/Status/i)).toBeInTheDocument();
    
    // Check for script data
    expect(await screen.findByText(/Test Script/i)).toBeInTheDocument();
    expect(await screen.findByText(/test keywords/i)).toBeInTheDocument();
    expect(await screen.findByText(/0 \* \* \* \*/i)).toBeInTheDocument();
    
    // Check for action buttons
    expect(screen.getByText(/Disable/i)).toBeInTheDocument();
    expect(screen.getByText(/Edit/i)).toBeInTheDocument();
    expect(screen.getByText(/Delete/i)).toBeInTheDocument();
  });
  
  test('displays empty state when no scripts', () => {
    // Override the mock to return empty array
    jest.mock('../contexts/ApiContext', () => ({
      useApi: () => ({
        isLoading: false,
        scripts: {
          getAll: jest.fn().mockResolvedValue([]),
          toggle: jest.fn(),
          update: jest.fn(),
          create: jest.fn(),
          delete: jest.fn()
        }
      }),
    }), { virtual: true });
    
    render(<ScriptManagement />);
    
    // Check for empty state message
    expect(screen.getByText(/No search scripts found/i)).toBeInTheDocument();
  });
  
  test('opens create script modal when create button is clicked', () => {
    render(<ScriptManagement />);
    
    // Click create button
    fireEvent.click(screen.getByText(/Create New Script/i));
    
    // Check if modal is open
    expect(screen.getByText(/Create New Script/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Script Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Schedule/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Keywords/i)).toBeInTheDocument();
  });
});
