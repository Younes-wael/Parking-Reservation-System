using Microsoft.EntityFrameworkCore;
using ParkingReservationSystem.Domain;
using ParkingReservationSystem.Infrastructure;

namespace ParkingReservationSystem.Services;

public class ReservationService
{
    private readonly AppDbContext _db;
    private readonly AvailabilityService _availabilityService;

    public ReservationService(AppDbContext db, AvailabilityService availabilityService)
    {
        _db = db;
        _availabilityService = availabilityService;
    }

    public async Task<Reservation?> CreateAsync(CreateReservationDto dto, int userId, CancellationToken ct = default)
    {
        var availability = await _availabilityService.GetAvailabilityAsync(dto.StartDate, dto.EndDate, ct);
        if (!availability.IsAvailableForEntireRange) return null;

        var reservation = new Reservation
        {
            GuestName = dto.GuestName,
            VehiclePlate = dto.VehiclePlate,
            StartDate = dto.StartDate,
            EndDate = dto.EndDate,
            Notes = dto.Notes,
            Status = ReservationStatus.Active,
            CreatedByUserId = userId,
            CreatedAt = DateTime.UtcNow
        };
        _db.Reservations.Add(reservation);
        await _db.SaveChangesAsync(ct);
        return reservation;
    }
}
