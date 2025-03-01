import { fireEvent, render, screen } from "@testing-library/react";
import FilterControls from "../../../components/resources/FilterControls";
import { ResourceFilters } from "../../../types/resource";

describe("FilterControls Component", () => {
  const initialFilters: ResourceFilters = {
    owner_id: null,
    is_public: null,
    search: "",
  };

  const mockOnChange = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders all filter controls", () => {
    render(
      <FilterControls
        filters={initialFilters}
        onChange={mockOnChange}
        showOwnerFilter={true}
      />
    );

    // Check if all filter controls are rendered
    expect(screen.getByLabelText(/Search/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Owner/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Visibility/i)).toBeInTheDocument();
    expect(screen.getByText(/Apply Filters/i)).toBeInTheDocument();
    expect(screen.getByText(/Reset/i)).toBeInTheDocument();
  });

  test("does not render owner filter when showOwnerFilter is false", () => {
    render(
      <FilterControls
        filters={initialFilters}
        onChange={mockOnChange}
        showOwnerFilter={false}
      />
    );

    // Check if owner filter is not rendered
    expect(screen.queryByLabelText(/Owner/i)).not.toBeInTheDocument();
  });

  test("updates search filter on input change", () => {
    render(<FilterControls filters={initialFilters} onChange={mockOnChange} />);

    // Type in search input
    const searchInput = screen.getByLabelText(/Search/i);
    fireEvent.change(searchInput, { target: { value: "test search" } });

    // Check if local state is updated (we can't directly check this, but we can check if the input value changed)
    expect(searchInput).toHaveValue("test search");
  });

  test("updates visibility filter on select change", () => {
    render(<FilterControls filters={initialFilters} onChange={mockOnChange} />);

    // Change visibility select
    const visibilitySelect = screen.getByLabelText(/Visibility/i);
    fireEvent.change(visibilitySelect, { target: { value: "true" } });

    // Check if local state is updated
    expect(visibilitySelect).toHaveValue("true");
  });

  test("updates owner filter on select change", () => {
    render(
      <FilterControls
        filters={initialFilters}
        onChange={mockOnChange}
        showOwnerFilter={true}
      />
    );

    // Change owner select
    const ownerSelect = screen.getByLabelText(/Owner/i);
    fireEvent.change(ownerSelect, { target: { value: "current" } });

    // Check if local state is updated
    expect(ownerSelect).toHaveValue("current");
  });

  test("calls onChange with updated filters when Apply Filters button is clicked", () => {
    render(<FilterControls filters={initialFilters} onChange={mockOnChange} />);

    // Update filters
    fireEvent.change(screen.getByLabelText(/Search/i), {
      target: { value: "test search" },
    });
    fireEvent.change(screen.getByLabelText(/Visibility/i), {
      target: { value: "true" },
    });

    // Click Apply Filters button
    fireEvent.click(screen.getByText(/Apply Filters/i));

    // Check if onChange was called with updated filters
    expect(mockOnChange).toHaveBeenCalledWith({
      ...initialFilters,
      search: "test search",
      is_public: true,
    });
  });

  test("calls onChange with reset filters when Reset button is clicked", () => {
    const filtersWithValues: ResourceFilters = {
      owner_id: 1,
      is_public: true,
      search: "test",
    };

    render(
      <FilterControls
        filters={filtersWithValues}
        onChange={mockOnChange}
        showOwnerFilter={true}
      />
    );

    // Click Reset button
    fireEvent.click(screen.getByText(/Reset/i));

    // Check if onChange was called with reset filters
    expect(mockOnChange).toHaveBeenCalledWith({
      owner_id: null,
      is_public: null,
      search: "",
    });
  });
});
