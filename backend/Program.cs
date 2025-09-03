using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using ParkingReservationSystem.Domain;
using ParkingReservationSystem.Infrastructure;
using ParkingReservationSystem.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseInMemoryDatabase("parking"));

builder.Services.AddScoped<AvailabilityService>();
builder.Services.AddScoped<ReservationService>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    DbSeeder.Seed(db);
}

app.MapGet("/api/availability", async (DateOnly start, DateOnly end, AvailabilityService service, CancellationToken ct) =>
{
    return await service.GetAvailabilityAsync(start, end, ct);
});

app.MapPost("/api/reservations", async (CreateReservationDto dto, ReservationService service) =>
{
    var reservation = await service.CreateAsync(dto, 1);
    return reservation is null ? Results.BadRequest(new { message = "No capacity" }) : Results.Ok(reservation);
});

app.Run();
