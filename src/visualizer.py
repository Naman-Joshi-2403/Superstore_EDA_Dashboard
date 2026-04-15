import pandas as pd


def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby(["Order Year", "Order Month"])["Sales"]
        .sum()
        .reset_index()
        .pivot(index="Order Month", columns="Order Year", values="Sales")
        .fillna(0)
    )
    out.index = ["Jan","Feb","Mar","Apr","May","Jun",
                 "Jul","Aug","Sep","Oct","Nov","Dec"][:len(out)]
    out.columns = [str(c) for c in out.columns]
    return out


def sales_by_category_year(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby(["Order Year", "Category"])["Sales"]
        .sum()
        .reset_index()
        .pivot(index="Order Year", columns="Category", values="Sales")
        .fillna(0)
    )
    out.index = [str(i) for i in out.index]
    return out


def quarterly_profit(df: pd.DataFrame) -> pd.DataFrame:
    tmp = df.copy()
    tmp["Period"] = tmp["Order Year"].astype(str) + "-Q" + tmp["Order Quarter"].astype(str)
    out = (
        tmp.groupby(["Period", "Category"])["Profit"]
        .sum()
        .reset_index()
        .pivot(index="Period", columns="Category", values="Profit")
        .fillna(0)
        .sort_index()
    )
    return out


def profit_by_subcategory(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values()
        .reset_index()
        .rename(columns={"Profit": "Total Profit"})
        .set_index("Sub-Category")
    )


def avg_profit_by_discount_tier(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Discount Tier", observed=True)["Profit"]
        .mean()
        .reset_index()
        .rename(columns={"Profit": "Avg Profit"})
        .set_index("Discount Tier")
    )


def loss_rate_by_discount_tier(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("Discount Tier", observed=True)["Is Loss"]
        .mean()
        .mul(100)
        .reset_index()
        .rename(columns={"Is Loss": "Loss Rate %"})
        .set_index("Discount Tier")
    )
    return out

def sales_profit_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Region")[["Sales", "Profit"]]
        .sum()
        .sort_values("Sales", ascending=False)
    )


def profit_by_state(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("State")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .set_index("State")
    )


def sales_by_region_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["Region", "Category"])["Profit"]
        .sum()
        .unstack(fill_value=0)
    )

def sales_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
        .set_index("Segment")
    )


def profit_margin_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Segment")["Profit Margin %"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"Profit Margin %": "Avg Profit Margin %"})
        .set_index("Segment")
    )


def top_customers(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .nlargest(n)
        .sort_values()
        .reset_index()
        .rename(columns={"Sales": "Total Sales"})
        .set_index("Customer Name")
    )

def avg_shipping_days(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Ship Mode")["Shipping Days"]
        .mean()
        .round(1)
        .sort_values()
        .reset_index()
        .rename(columns={"Shipping Days": "Avg Shipping Days"})
        .set_index("Ship Mode")
    )


def avg_profit_by_ship_mode(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Ship Mode")["Profit"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"Profit": "Avg Profit"})
        .set_index("Ship Mode")
    )


def shipping_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("Ship Mode")
        .agg(
            Orders=("Row ID", "count"),
            Avg_Days=("Shipping Days", "mean"),
            Avg_Profit=("Profit", "mean"),
            Loss_Rate=("Is Loss", "mean"),
        )
        .round(2)
        .reset_index()
    )
    out["Avg_Days"]   = out["Avg_Days"].apply(lambda x: f"{x:.1f} days")
    out["Avg_Profit"] = out["Avg_Profit"].apply(lambda x: f"${x:.2f}")
    out["Loss_Rate"]  = out["Loss_Rate"].apply(lambda x: f"{x*100:.1f}%")
    out.columns = ["Ship Mode", "Orders", "Avg Days", "Avg Profit", "Loss Rate"]
    return out.set_index("Ship Mode")

def correlation_table(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[["Sales", "Quantity", "Discount", "Profit", "Shipping Days", "Profit Margin %"]]
        .corr()
        .round(2)
    )
