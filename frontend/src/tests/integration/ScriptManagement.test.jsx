import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ApiProvider } from '../contexts/ApiContext';
import ScriptManagement from '../pages/ScriptManagement';

// Mock the API services
jest.mock('../api/services', () => ({
  __esModule: true,
  default: {
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
      toggle: jest.fn().mockResolvedValue({
        id: 1,
        name: 'Test Script',
        is_active: false
      }),
      create: jest.fn().mockImplementation((script) => Promise.resolve({
        id: 2,
        ...script,
        created_at: '2025-04-14T12:00:00Z',
        updated_at: '2025-04-14T12:00:00Z'
      })),
      update: jest.fn().mockImplementation((id, script) => Promise.resolve({
        id,
        ...script,
        updated_at: '2025-04-14T12:00:00Z'
      })),
      delete: jest.fn().mockResolvedValue(true)
    }
  }
}));

describe('ScriptManagement Integration Test', () => {
  test('fetches scripts from API and displays them', async () => {
    render(
      <ApiProvider>
        <ScriptManagement />
      </ApiProvider>
    );
    
    // Wait for scripts to load
    await waitFor(() => {
      expect(screen.getByText(/Test Script/i)).toBeInTheDocument();
    });
    
    // Verify API service was called
    expect(require('../api/services').default.scripts.getAll).toHaveBeenCalled();
  });
  
  test('toggles script active status via API', async () => {
    render(
      <ApiProvider>
        <ScriptManagement />
      </ApiProvider>
    );
    
    // Wait for scripts to load
    await waitFor(() => {
      expect(screen.getByText(/Test Script/i)).toBeInTheDocument();
    });
    
    // Click the toggle button
    fireEvent.click(screen.getByText(/Disable/i));
    
    // Verify API service was called
    await waitFor(() => {
      expect(require('../api/services').default.scripts.toggle).toHaveBeenCalledWith(1);
    });
  });
  
  test('creates new script via API', async () => {
    render(
      <ApiProvider>
        <ScriptManagement />
      </ApiProvider>
    );
    
    // Click create button
    fireEvent.click(screen.getByText(/Create New Script/i));
    
    // Fill out the form
    fireEvent.change(screen.getByLabelText(/Script Name/i), {
      target: { value: 'New Test Script' }
    });
    
    fireEvent.change(screen.getByLabelText(/Keywords/i), {
      target: { value: 'new test keywords' }
    });
    
    // Submit the form
    fireEvent.click(screen.getByText(/Create Script/i));
    
    // Verify API service was called with correct data
    await waitFor(() => {
      expect(require('../api/services').default.scripts.create).toHaveBeenCalled();
      const createCall = require('../api/services').default.scripts.create.mock.calls[0][0];
      expect(createCall.name).toBe('New Test Script');
      expect(createCall.search_parameters.keywords).toBe('new test keywords');
    });
  });
});
