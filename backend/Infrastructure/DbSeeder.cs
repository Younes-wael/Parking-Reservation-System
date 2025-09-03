using ParkingReservationSystem.Domain;

namespace ParkingReservationSystem.Infrastructure;

public static class DbSeeder
{
    public static void Seed(AppDbContext db)
    {
        if (!db.Users.Any())
        {
            db.Users.Add(new User
            {
                Username = "admin",
                PasswordHash = "hashed-password",
                Role = "Admin",
                CreatedAt = DateTime.UtcNow,
                IsActive = true
            });
        }

        if (!db.Reservations.Any())
        {
            var today = DateOnly.FromDateTime(DateTime.UtcNow);
            var rnd = new Random(0);
            for (int i = 0; i < 50; i++)
            {
                var start = today.AddDays(rnd.Next(0, 60));
                var end = start.AddDays(rnd.Next(0, 5));
                db.Reservations.Add(new Reservation
                {
                    GuestName = $"Guest{i}",
                    VehiclePlate = $"PLT{i:000}",
                    StartDate = start,
                    EndDate = end,
                    Status = ReservationStatus.Active,
                    CreatedByUserId = 1,
                    CreatedAt = DateTime.UtcNow
                });
            }
        }

        db.SaveChanges();
    }
}
