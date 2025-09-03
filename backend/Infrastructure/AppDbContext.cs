using Microsoft.EntityFrameworkCore;
using ParkingReservationSystem.Domain;

namespace ParkingReservationSystem.Infrastructure;

public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();
    public DbSet<Reservation> Reservations => Set<Reservation>();
    public DbSet<CapacitySetting> CapacitySettings => Set<CapacitySetting>();
    public DbSet<AuditLog> AuditLogs => Set<AuditLog>();

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>().HasIndex(u => u.Username).IsUnique();
        modelBuilder.Entity<Reservation>().HasIndex(r => new { r.StartDate, r.EndDate });
    }
}
