namespace ParkingReservationSystem.Domain;

public enum ReservationStatus { Active, Cancelled }
public enum AuditAction { Create, Update, Cancel }

public class User
{
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string Role { get; set; } = "Agent";
    public DateTime CreatedAt { get; set; }
    public bool IsActive { get; set; } = true;
}

public class Reservation
{
    public int Id { get; set; }
    public string GuestName { get; set; } = string.Empty;
    public string VehiclePlate { get; set; } = string.Empty;
    public DateOnly StartDate { get; set; }
    public DateOnly EndDate { get; set; }
    public ReservationStatus Status { get; set; } = ReservationStatus.Active;
    public string? Notes { get; set; }
    public int CreatedByUserId { get; set; }
    public DateTime CreatedAt { get; set; }
    public int? UpdatedByUserId { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public DateTime? CancelledAt { get; set; }
}

public class CapacitySetting
{
    public int Id { get; set; }
    public DateOnly Date { get; set; }
    public int? OverrideTotal { get; set; }
}

public class AuditLog
{
    public int Id { get; set; }
    public string EntityName { get; set; } = string.Empty;
    public int EntityId { get; set; }
    public AuditAction Action { get; set; }
    public int ChangedByUserId { get; set; }
    public DateTime ChangedAt { get; set; }
    public string DiffJson { get; set; } = string.Empty;
}
