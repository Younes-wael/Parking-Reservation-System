using Microsoft.EntityFrameworkCore.Migrations;

namespace ParkingReservationSystem.Infrastructure.Migrations;

public partial class InitialCreate : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Users",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                Username = table.Column<string>(nullable: false),
                PasswordHash = table.Column<string>(nullable: false),
                Role = table.Column<string>(nullable: false),
                CreatedAt = table.Column<DateTime>(nullable: false),
                IsActive = table.Column<bool>(nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Users", x => x.Id);
            });

        migrationBuilder.CreateTable(
            name: "Reservations",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                GuestName = table.Column<string>(nullable: false),
                VehiclePlate = table.Column<string>(nullable: false),
                StartDate = table.Column<DateOnly>(type: "date", nullable: false),
                EndDate = table.Column<DateOnly>(type: "date", nullable: false),
                Status = table.Column<int>(nullable: false),
                Notes = table.Column<string>(nullable: true),
                CreatedByUserId = table.Column<int>(nullable: false),
                CreatedAt = table.Column<DateTime>(nullable: false),
                UpdatedByUserId = table.Column<int>(nullable: true),
                UpdatedAt = table.Column<DateTime>(nullable: true),
                CancelledAt = table.Column<DateTime>(nullable: true)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Reservations", x => x.Id);
            });

        migrationBuilder.CreateTable(
            name: "CapacitySettings",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                Date = table.Column<DateOnly>(type: "date", nullable: false),
                OverrideTotal = table.Column<int>(nullable: true)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_CapacitySettings", x => x.Id);
            });

        migrationBuilder.CreateTable(
            name: "AuditLogs",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                EntityName = table.Column<string>(nullable: false),
                EntityId = table.Column<int>(nullable: false),
                Action = table.Column<int>(nullable: false),
                ChangedByUserId = table.Column<int>(nullable: false),
                ChangedAt = table.Column<DateTime>(nullable: false),
                DiffJson = table.Column<string>(nullable: false)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_AuditLogs", x => x.Id);
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable("AuditLogs");
        migrationBuilder.DropTable("CapacitySettings");
        migrationBuilder.DropTable("Reservations");
        migrationBuilder.DropTable("Users");
    }
}
