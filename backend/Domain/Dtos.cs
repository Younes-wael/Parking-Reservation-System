namespace ParkingReservationSystem.Domain;

public record AvailabilityDto(DateOnly Date, int Booked, int Capacity, int Remaining);
public record AvailabilityResponse(IEnumerable<AvailabilityDto> Days, bool IsAvailableForEntireRange);

public record CreateReservationDto(string GuestName, string VehiclePlate, DateOnly StartDate, DateOnly EndDate, string? Notes);

