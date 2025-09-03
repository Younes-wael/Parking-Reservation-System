using ParkingReservationSystem.Domain;
using ParkingReservationSystem.Infrastructure;
using ParkingReservationSystem.Services;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ParkingReservationSystem.Tests;

public class AvailabilityServiceTests
{
    private static AppDbContext CreateContext()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        return new AppDbContext(options);
    }

    [Fact]
    public async Task ReturnsCapacityAndBookings()
    {
        using var ctx = CreateContext();
        ctx.Reservations.Add(new Reservation
        {
            GuestName = "A",
            VehiclePlate = "AAA",
            StartDate = new DateOnly(2024,1,10),
            EndDate = new DateOnly(2024,1,12),
            Status = ReservationStatus.Active,
            CreatedByUserId = 1,
            CreatedAt = DateTime.UtcNow
        });
        await ctx.SaveChangesAsync();

        var service = new AvailabilityService(ctx);
        var result = await service.GetAvailabilityAsync(new DateOnly(2024,1,9), new DateOnly(2024,1,11));
        var day = result.Days.First(d => d.Date == new DateOnly(2024,1,10));
        Assert.Equal(1, day.Booked);
    }
}
