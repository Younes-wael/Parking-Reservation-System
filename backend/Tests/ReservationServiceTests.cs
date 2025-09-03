using ParkingReservationSystem.Domain;
using ParkingReservationSystem.Infrastructure;
using ParkingReservationSystem.Services;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ParkingReservationSystem.Tests;

public class ReservationServiceTests
{
    private static AppDbContext CreateContext()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        return new AppDbContext(options);
    }

    [Fact]
    public async Task OverbookingReturnsNull()
    {
        using var ctx = CreateContext();
        ctx.CapacitySettings.Add(new CapacitySetting { Date = new DateOnly(2024,1,1), OverrideTotal = 1 });
        ctx.Reservations.Add(new Reservation
        {
            GuestName = "A",
            VehiclePlate = "AAA",
            StartDate = new DateOnly(2024,1,1),
            EndDate = new DateOnly(2024,1,1),
            Status = ReservationStatus.Active,
            CreatedByUserId = 1,
            CreatedAt = DateTime.UtcNow
        });
        await ctx.SaveChangesAsync();

        var availability = new AvailabilityService(ctx);
        var service = new ReservationService(ctx, availability);
        var result = await service.CreateAsync(
            new CreateReservationDto("B","BBB", new DateOnly(2024,1,1), new DateOnly(2024,1,1), null), 1);
        Assert.Null(result);
    }
}
