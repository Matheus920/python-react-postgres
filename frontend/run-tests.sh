#!/bin/bash

# Script to run frontend tests

echo "Running frontend tests..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing dependencies..."
  npm install
fi

# Run tests with coverage
echo "Running tests with coverage..."
npm run test:coverage

# Check test results
if [ $? -eq 0 ]; then
  echo "✅ All tests passed!"
else
  echo "❌ Some tests failed. Please check the output above for details."
  exit 1
fi

echo "Test coverage report is available in the coverage directory."
echo "Open coverage/lcov-report/index.html in a browser to view the detailed report."
