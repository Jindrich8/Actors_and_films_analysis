# data_utils
from typing import Iterable
import polars as pl
import pandas as pd
from polars.expr.list import ExprListNameSpace

type PolarsAnyDataFrame = pl.DataFrame|pl.LazyFrame
type AnyDataFrame = PolarsAnyDataFrame | pd.DataFrame

def load_lazy(path: str,separator:str,list_sep=",", schema: dict = None,has_header=True, null_values="\\N",strip_list_encapsulation:tuple[str,str] = ("[","]"),strip_list_item_encapsulation:tuple[str,str] = ('"','"')) -> pl.LazyFrame:
    """
    Lazily load a CSV/TSV using Polars, respecting schema and nulls.
    Automatically parses columns typed as List(Utf8) using str.split(',')

    Args:
        path: Path to TSV/CSV
        separator: Single byte character to use as separator in the file
        list_sep: String used to seperate list values in the file
        schema: Optional dict of column_name -> pl.DataType
        has_header: Indicate if the first row of the dataset is a header or not
        null_values: String or list of strings representing nulls
        strip_list_encapsulation: Strings that may encapsulate list value.
        strip_list_item_encapsulation: Strings that may encapsulate list item value.

    Returns:
        pl.LazyFrame
    """
    load_schema = {
    k: (v.inner if isinstance(v, pl.List) else v)
    for k, v in schema.items()
}
    df_lazy = pl.scan_csv(
        path,
        separator=separator,
        null_values=null_values,
        has_header=has_header,
        quote_char=None,
        schema_overrides=load_schema,
        ignore_errors=False
    )
    if schema is not None:
        # Detect all list columns in schema
        list_cols = [col for col, dtype in schema.items() if isinstance(dtype, pl.List)]
        if list_cols:
            # Apply str.split to all list columns lazily
            df_lazy = df_lazy.with_columns([
                pl.col(c).str.strip_prefix(strip_list_encapsulation[0])\
                    .str.strip_suffix(strip_list_encapsulation[1])\
                        .str.split(list_sep)\
                            .list.eval(
                                pl.element().str.strip_prefix(strip_list_item_encapsulation[0])\
                                    .str.strip_suffix(strip_list_item_encapsulation[1])
                                ) for c in list_cols
                        ])

    return df_lazy

def as_lazy(df:PolarsAnyDataFrame)->pl.LazyFrame:
    """Converts given data frame to LazyFrame if needed.

    Args:
        df (pl.DataFrame | pl.LazyFrame): Data frame to convert to lazy data frame

    Returns:
        pl.LazyFrame: Lazy data frame corresponding to given data frame
    """
    return df.lazy() if isinstance(df,pl.DataFrame) else df

def count(iter:Iterable)->int:
    count = 0
    for _ in iter:
        count+=1
    return count

def collect_if_lazy(df):
    if(isinstance(df,pl.LazyFrame)):
        df = df.collect()
    return df

def df_to_html(df:AnyDataFrame,title:str|None=None,hide_index:bool = True)->str:
    CAPTION_STYLE = "font-size:large; font-weight: bolder; margin: 1rem;"
    if isinstance(df,pd.DataFrame):
        styler = (df.style.hide(axis="index") if hide_index else df.style)
        
        return (styler if title == None else styler.set_table_styles([{
        "selector":"caption",
        "props":CAPTION_STYLE
        }]).set_caption(title)).to_html()
    else:
        import re
        html = collect_if_lazy(df)._repr_html_()
        if title != None:
            insert_index = re.search("<\\s*table[^>]*>",html).span()[1]
            html = html[:insert_index] + f"<caption style='{CAPTION_STYLE}'>{title}</caption>" + html[insert_index:]
        return html

def display_html(str:str):
    from IPython.display import display, HTML
    display(HTML(str))

def display_with_title(title:str,df:pd.DataFrame|pl.LazyFrame|pl.DataFrame,hide_index:bool = True):
    display_html(df_to_html(df,title,hide_index))

def display_side_by_side(*dfs:AnyDataFrame|tuple[str,AnyDataFrame],hide_index:bool = True):
    title_w_df = map(lambda df: (None,df) if not isinstance(df,tuple) else df,dfs)
    
    display_html(
        "<div style='display:flex; flex-wrap:wrap; gap:30px;'>"+"".join(
            map(lambda title_w_df: df_to_html(
                title= title_w_df[0],
                df=title_w_df[1],
                hide_index=hide_index
                ),
                title_w_df
                )
            )+"</div>")
    

import polars as pl

def prepare_degree_data(df_counts: pl.DataFrame, degree_col: str, count_col: str = 'count', xtick_step: int = 10):
    """
    Prepare x and height lists for plotting a degree-like distribution.
    Fills missing degrees with 0.
    Returns x, height, xticks
    """
    min_deg = df_counts[degree_col].min()
    max_deg = df_counts[degree_col].max()

    # doplníme chybějící stupně
    full_degrees = pl.DataFrame({degree_col: list(range(0, max_deg + 1))})
    full_counts = full_degrees.join(df_counts, on=degree_col, how='left').fill_null(0)

    x = full_counts[degree_col].to_list()
    height = full_counts[count_col].to_list()

    # xticks: min, multiples xtick_step, max
    ticks = list(range(0, max_deg + 1, xtick_step))
    if min_deg not in ticks:
        ticks = [min_deg] + ticks
    if max_deg not in ticks:
        ticks.append(max_deg)

    return x, height, ticks