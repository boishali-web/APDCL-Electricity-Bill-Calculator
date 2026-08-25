# ============================================================
# APDCL ELECTRICITY BILL CALCULATOR
# Tariff Year: 2026-27
# ============================================================

ELECTRICITY_DUTY = 0.05       # 5%
FPPPA_RATE = 0.20             # Example: ₹0.20/unit
SOLAR_REBATE = 0.20           # 20%


# ------------------------------------------------------------
# DOMESTIC-A TARIFF
# ------------------------------------------------------------

DOMESTIC_A_SLABS = [
    (120, 4.25),
    (240, 6.30),
    (300, 7.20),
    (500, 7.40),
    (float("inf"), 8.19)
]

DOMESTIC_A_FIXED_CHARGE = 70


# ------------------------------------------------------------
# DOMESTIC-B TARIFF
# ------------------------------------------------------------

DOMESTIC_B_SLABS = [
    (200, 6.75),
    (500, 7.50),
    (float("inf"), 8.50)
]

DOMESTIC_B_FIXED_CHARGE = 70


# ------------------------------------------------------------
# COMMERCIAL TARIFF
# ------------------------------------------------------------

COMMERCIAL_RATE = 8.94
COMMERCIAL_FIXED_CHARGE_PER_KW = 150


# ------------------------------------------------------------
# FUNCTION TO CALCULATE TELESCOPIC BILL
# ------------------------------------------------------------

def calculate_slab_charge(units, slabs):

    remaining_units = units
    energy_charge = 0
    previous_limit = 0

    for upper_limit, rate in slabs:

        slab_units = min(
            remaining_units,
            upper_limit - previous_limit
        )

        if slab_units <= 0:
            break

        charge = slab_units * rate
        energy_charge += charge

        remaining_units -= slab_units
        previous_limit = upper_limit

        if remaining_units <= 0:
            break

    return energy_charge


# ------------------------------------------------------------
# MAIN BILL CALCULATION
# ------------------------------------------------------------

def calculate_bill():

    print("\n" + "=" * 55)
    print("          APDCL ELECTRICITY BILL CALCULATOR")
    print("=" * 55)

    print("\nSelect Connection Type:")
    print("1. Domestic-A")
    print("2. Domestic-B")
    print("3. Commercial")

    while True:
        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice in ["1", "2", "3"]:
            break

        print("Invalid choice. Please enter 1, 2 or 3.")

    # --------------------------------------------------------
    # GET UNIT CONSUMPTION
    # --------------------------------------------------------

    while True:

        try:
            units = float(
                input("Enter electricity consumption (units): ")
            )

            if units < 0:
                print("Units cannot be negative.")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    # --------------------------------------------------------
    # DOMESTIC-A
    # --------------------------------------------------------

    if choice == "1":

        category = "Domestic-A"

        energy_charge = calculate_slab_charge(
            units,
            DOMESTIC_A_SLABS
        )

        fixed_charge = DOMESTIC_A_FIXED_CHARGE

    # --------------------------------------------------------
    # DOMESTIC-B
    # --------------------------------------------------------

    elif choice == "2":

        category = "Domestic-B"

        energy_charge = calculate_slab_charge(
            units,
            DOMESTIC_B_SLABS
        )

        fixed_charge = DOMESTIC_B_FIXED_CHARGE

    # --------------------------------------------------------
    # COMMERCIAL
    # --------------------------------------------------------

    else:

        category = "Commercial"

        while True:

            try:
                load = float(
                    input("Enter sanctioned load (kW): ")
                )

                if load <= 0:
                    print("Load must be greater than zero.")
                else:
                    break

            except ValueError:
                print("Please enter a valid load.")

        energy_charge = units * COMMERCIAL_RATE

        fixed_charge = (
            load * COMMERCIAL_FIXED_CHARGE_PER_KW
        )

    # --------------------------------------------------------
    # FPPPA
    # --------------------------------------------------------

    fpppa_charge = units * FPPPA_RATE

    # --------------------------------------------------------
    # ELECTRICITY DUTY
    # --------------------------------------------------------

    electricity_duty = (
        energy_charge * ELECTRICITY_DUTY
    )

    # --------------------------------------------------------
    # TOTAL BILL
    # --------------------------------------------------------

    total_bill = (
        energy_charge
        + fixed_charge
        + fpppa_charge
        + electricity_duty
    )

    # --------------------------------------------------------
    # DISPLAY BILL
    # --------------------------------------------------------

    print("\n" + "=" * 55)
    print("                 BILL SUMMARY")
    print("=" * 55)

    print(f"Connection Type       : {category}")
    print(f"Units Consumed        : {units:.2f} kWh")

    print("-" * 55)

    print(f"Energy Charge         : ₹{energy_charge:.2f}")
    print(f"Fixed Charge          : ₹{fixed_charge:.2f}")
    print(f"FPPPA Charge          : ₹{fpppa_charge:.2f}")
    print(f"Electricity Duty (5%) : ₹{electricity_duty:.2f}")

    print("-" * 55)

    print(f"TOTAL BILL            : ₹{total_bill:.2f}")

    print("=" * 55)


# ------------------------------------------------------------
# RUN PROGRAM
# ------------------------------------------------------------

calculate_bill()
