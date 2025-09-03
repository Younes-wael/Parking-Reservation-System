using Microsoft.EntityFrameworkCore;
using ParkingReservationSystem.Domain;
using ParkingReservationSystem.Infrastructure;

namespace ParkingReservationSystem.Services;

public class AvailabilityService
{
    private const int DefaultCapacity = 50;
    private readonly AppDbContext _db;

    public AvailabilityService(AppDbContext db) => _db = db;

    public async Task<AvailabilityResponse> GetAvailabilityAsync(DateOnly start, DateOnly end, CancellationToken ct = default)
    {
        var days = Enumerable.Range(0, end.DayNumber - start.DayNumber + 1)
            .Select(offset => start.AddDays(offset))
            .ToList();

        var reservations = await _db.Reservations
            .Where(r => r.Status == ReservationStatus.Active && r.StartDate <= end && r.EndDate >= start)
            .ToListAsync(ct);

        var overrides = await _db.CapacitySettings
            .Where(c => c.Date >= start && c.Date <= end)
            .ToDictionaryAsync(c => c.Date, ct);

        var results = new List<AvailabilityDto>();
        var isAvailable = true;
        foreach (var day in days)
        {
            var booked = reservations.Count(r => r.StartDate <= day && r.EndDate >= day);
            var capacity = overrides.TryGetValue(day, out var ov) && ov.OverrideTotal.HasValue ? ov.OverrideTotal.Value : DefaultCapacity;
            var remaining = capacity - booked;
            if (remaining < 1) isAvailable = false;
            results.Add(new AvailabilityDto(day, booked, capacity, remaining));
        }

        return new AvailabilityResponse(results, isAvailable);
    }
}
