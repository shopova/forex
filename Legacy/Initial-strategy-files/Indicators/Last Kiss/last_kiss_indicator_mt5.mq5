#property strict
#property indicator_chart_window
#property indicator_plots 12
#property indicator_buffers 12

#property indicator_label1  "Box Top"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrDarkOrange
#property indicator_style1  STYLE_SOLID
#property indicator_width1  2

#property indicator_label2  "Box Bottom"
#property indicator_type2   DRAW_LINE
#property indicator_color2  clrDarkOrange
#property indicator_style2  STYLE_SOLID
#property indicator_width2  2

#property indicator_label3  "Support Zone"
#property indicator_type3   DRAW_LINE
#property indicator_color3  clrSeaGreen
#property indicator_style3  STYLE_DOT
#property indicator_width3  1

#property indicator_label4  "Resistance Zone"
#property indicator_type4   DRAW_LINE
#property indicator_color4  clrIndianRed
#property indicator_style4  STYLE_DOT
#property indicator_width4  1

#property indicator_label5  "Pending Entry"
#property indicator_type5   DRAW_LINE
#property indicator_color5  clrDodgerBlue
#property indicator_style5  STYLE_SOLID
#property indicator_width5  2

#property indicator_label6  "Emergency Stop"
#property indicator_type6   DRAW_LINE
#property indicator_color6  clrCrimson
#property indicator_style6  STYLE_SOLID
#property indicator_width6  2

#property indicator_label7  "Target"
#property indicator_type7   DRAW_LINE
#property indicator_color7  clrLimeGreen
#property indicator_style7  STYLE_SOLID
#property indicator_width7  2

#property indicator_label8  "Bull Setup"
#property indicator_type8   DRAW_ARROW
#property indicator_color8  clrDeepSkyBlue
#property indicator_style8  STYLE_SOLID
#property indicator_width8  1

#property indicator_label9  "Bear Setup"
#property indicator_type9   DRAW_ARROW
#property indicator_color9  clrDeepSkyBlue
#property indicator_style9  STYLE_SOLID
#property indicator_width9  1

#property indicator_label10 "Bull Entry"
#property indicator_type10  DRAW_ARROW
#property indicator_color10 clrLimeGreen
#property indicator_style10 STYLE_SOLID
#property indicator_width10 1

#property indicator_label11 "Bear Entry"
#property indicator_type11  DRAW_ARROW
#property indicator_color11 clrTomato
#property indicator_style11 STYLE_SOLID
#property indicator_width11 1

#property indicator_label12 "Canceled"
#property indicator_type12  DRAW_ARROW
#property indicator_color12 clrGray
#property indicator_style12 STYLE_SOLID
#property indicator_width12 1

enum PairPresetMode
  {
   PAIR_PRESET_OFF = 0,   // Off (Manual Inputs)
   PAIR_PRESET_SYNC = 1   // Synced Per-Pair (MT5 2020-2026, 2026-02-26)
  };

enum StopMode
  {
   STOP_MIDPOINT = 0,         // Midpoint of Box
   STOP_OPPOSITE_EDGE = 1,    // Opposite Box Edge
   STOP_OPPOSITE_EDGE_ATR = 2 // Opposite Edge + ATR
  };

enum TargetMode
  {
   TARGET_NEAREST_ZONE = 0, // Nearest Zone
   TARGET_R_MULTIPLE = 1    // R Multiple
  };

input PairPresetMode InpPairPresetMode = PAIR_PRESET_OFF;

input int    InpMinConsolBars             = 20;
input int    InpMaxConsolBars             = 80;
input int    InpMinTouches                = 2;
input double InpTouchTolPct               = 8.0;
input int    InpTouchTolTicks             = 8;
input double InpRangeVolBufAtr            = 0.10;
input int    InpRangeVolBufTicks          = 5;
input int    InpRecentTouchWindow         = 12;
input int    InpMinRecentBoundaryTouches  = 2;
input int    InpMaxBoundaryStaleBars      = 30;
input double InpMaxConsolDriftPct         = 25.0;
input int    InpMaxOutsideCloses          = 1;
input int    InpMaxOutsideCloseRun        = 2;
input int    InpAtrLen                    = 14;
input double InpMinBoxAtr                 = 1.2;
input double InpMaxBoxAtr                 = 6.0;

input bool   InpBreakoutCloseOnly         = true;
input double InpBreakoutBufferAtr         = 0.10;
input double InpMinBreakoutBodyAtr        = 0.25;
input bool   InpUseVolumeFilter           = true;
input int    InpVolumeMALength            = 20;
input double InpVolumeMultiplier          = 1.1;
input int    InpMaxFakeBreakouts          = 2;

input int    InpMaxRetestBars             = 15;
input double InpRetestTolPct              = 12.0;
input int    InpRetestTolTicks            = 10;
input double InpMinCatalystBodyAtr        = 0.20;
input double InpCloseNearExtremePct       = 25.0;
input double InpMinWickBodyRatio          = 0.20;

input int       InpEntryOffsetTicks       = 2;
input int       InpEntryExpiryBars        = 5;
input StopMode  InpStopMode               = STOP_MIDPOINT;
input double    InpStopAtrMult            = 1.0;
input TargetMode InpTargetMode            = TARGET_R_MULTIPLE;
input double    InpTargetRR               = 2.0;
input double    InpMinSetupRR             = 2.0;
input int       InpTargetPivotLen         = 3;
input int       InpTargetZoneBufferTicks  = 2;

input bool InpUseTrendFilter              = true;
input int  InpDailySmaLen                 = 200;
input int  InpH4EmaLen                    = 50;
input bool InpUseSessionFilter            = true;
input int  InpSessionStartHour            = 7;
input int  InpSessionStartMinute          = 0;
input int  InpSessionEndHour              = 17;
input int  InpSessionEndMinute            = 0;

input bool InpShowBox                     = true;
input bool InpShowBoxArea                 = true;
input bool InpFreezeBoxOnBreakout         = true;
input int  InpMaxNoZoneTouchBars          = 120;
input bool InpShowLevels                  = true;
input bool InpShowTargetZones             = false;
input bool InpShowEventMarkers            = true;
input bool InpEnableAlerts                = true;

double g_boxTopBuffer[];
double g_boxBottomBuffer[];
double g_supportBuffer[];
double g_resistanceBuffer[];
double g_entryBuffer[];
double g_stopBuffer[];
double g_targetBuffer[];
double g_bullSetupBuffer[];
double g_bearSetupBuffer[];
double g_bullEntryBuffer[];
double g_bearEntryBuffer[];
double g_cancelBuffer[];

int g_atrHandle = INVALID_HANDLE;
int g_dailySmaHandle = INVALID_HANDLE;
int g_h4EmaHandle = INVALID_HANDLE;

string BOX_OBJECT_NAME = "LastKissActiveBox";

double MaxDouble(const double a,const double b)
  {
   return(a > b ? a : b);
  }

double MinDouble(const double a,const double b)
  {
   return(a < b ? a : b);
  }

string UpperSymbol()
  {
   string symbol = _Symbol;
   StringToUpper(symbol);
   return(symbol);
  }

bool SymbolContains(const string needle)
  {
   return(StringFind(UpperSymbol(),needle) >= 0);
  }

double VolumeAverage(const int index,
                     const int length,
                     const int rates_total,
                     const long &tick_volume[])
  {
   if(length <= 0 || index + length - 1 >= rates_total)
      return(0.0);

   double total = 0.0;
   for(int k = 0; k < length; ++k)
      total += (double)tick_volume[index + k];

   return(total / (double)length);
  }

bool ConfirmedPivotLow(const int confirm_index,
                       const int pivot_len,
                       const int rates_total,
                       const double &low[],
                       double &price)
  {
   int pivot_index = confirm_index + pivot_len;
   if(pivot_len < 1 || pivot_index + pivot_len >= rates_total)
      return(false);

   double pivot = low[pivot_index];
   for(int k = 1; k <= pivot_len; ++k)
     {
      if(low[pivot_index + k] <= pivot)
         return(false);
      if(low[pivot_index - k] < pivot)
         return(false);
     }

   price = pivot;
   return(true);
  }

bool ConfirmedPivotHigh(const int confirm_index,
                        const int pivot_len,
                        const int rates_total,
                        const double &high[],
                        double &price)
  {
   int pivot_index = confirm_index + pivot_len;
   if(pivot_len < 1 || pivot_index + pivot_len >= rates_total)
      return(false);

   double pivot = high[pivot_index];
   for(int k = 1; k <= pivot_len; ++k)
     {
      if(high[pivot_index + k] >= pivot)
         return(false);
      if(high[pivot_index - k] > pivot)
         return(false);
     }

   price = pivot;
   return(true);
  }

bool InTradeSession(const datetime bar_time,
                    const int start_hour,
                    const int start_minute,
                    const int end_hour,
                    const int end_minute)
  {
   int start_total = start_hour * 60 + start_minute;
   int end_total = end_hour * 60 + end_minute;

   if(start_total == end_total)
      return(true);

   MqlDateTime parts;
   TimeToStruct(bar_time,parts);
   int current_total = parts.hour * 60 + parts.min;

   if(start_total < end_total)
      return(current_total >= start_total && current_total < end_total);

   return(current_total >= start_total || current_total < end_total);
  }

bool CopySingleValue(const int handle,const int shift,double &value)
  {
   double temp[];
   ArrayResize(temp,1);
   if(CopyBuffer(handle,0,shift,1,temp) != 1)
      return(false);

   value = temp[0];
   return(true);
  }

bool GetTrendState(const datetime bar_time,bool &trend_long,bool &trend_short)
  {
   trend_long = false;
   trend_short = false;

   if(g_dailySmaHandle == INVALID_HANDLE || g_h4EmaHandle == INVALID_HANDLE)
      return(false);

   int daily_shift = iBarShift(_Symbol,PERIOD_D1,bar_time,false);
   int h4_shift = iBarShift(_Symbol,PERIOD_H4,bar_time,false);
   if(daily_shift < 0 || h4_shift < 0)
      return(false);

   double daily_sma = 0.0;
   double h4_ema = 0.0;
   if(!CopySingleValue(g_dailySmaHandle,daily_shift,daily_sma))
      return(false);
   if(!CopySingleValue(g_h4EmaHandle,h4_shift,h4_ema))
      return(false);

   double daily_close = iClose(_Symbol,PERIOD_D1,daily_shift);
   double h4_close = iClose(_Symbol,PERIOD_H4,h4_shift);
   if(daily_close == 0.0 || h4_close == 0.0)
      return(false);

   trend_long = (daily_close > daily_sma && h4_close > h4_ema);
   trend_short = (daily_close < daily_sma && h4_close < h4_ema);
   return(true);
  }

void ApplyPairPreset(int &min_consol_bars,
                     int &max_consol_bars,
                     int &min_touches,
                     double &touch_tol_pct,
                     double &range_vol_buf_atr,
                     int &range_vol_buf_ticks,
                     int &recent_touch_window,
                     int &min_recent_boundary_touches,
                     int &max_boundary_stale_bars,
                     double &max_consol_drift_pct,
                     int &max_outside_closes,
                     int &max_outside_close_run,
                     double &min_box_atr,
                     double &max_box_atr,
                     double &breakout_buffer_atr,
                     double &min_breakout_body_atr,
                     bool &use_volume_filter,
                     double &volume_multiplier,
                     int &max_retest_bars,
                     double &retest_tol_pct,
                     double &min_catalyst_body_atr,
                     double &close_near_extreme_pct,
                     double &min_wick_body_ratio,
                     int &entry_expiry_bars,
                     StopMode &stop_mode,
                     TargetMode &target_mode,
                     double &target_rr,
                     double &min_setup_rr,
                     bool &use_trend_filter,
                     bool &use_session_filter,
                     int &max_no_zone_touch_bars)
  {
   if(InpPairPresetMode != PAIR_PRESET_SYNC)
      return;

   if(SymbolContains("EURUSD"))
     {
      min_consol_bars = 16;
      max_consol_bars = 60;
      min_touches = 2;
      touch_tol_pct = 8.0;
      range_vol_buf_atr = 0.10;
      range_vol_buf_ticks = 5;
      recent_touch_window = 16;
      min_recent_boundary_touches = 2;
      max_boundary_stale_bars = 20;
      max_consol_drift_pct = 25.0;
      max_outside_closes = 1;
      max_outside_close_run = 1;
      min_box_atr = 1.2;
      max_box_atr = 4.0;
      breakout_buffer_atr = 0.15;
      min_breakout_body_atr = 0.35;
      use_volume_filter = true;
      volume_multiplier = 1.2;
      max_retest_bars = 12;
      retest_tol_pct = 10.0;
      min_catalyst_body_atr = 0.20;
      close_near_extreme_pct = 25.0;
      min_wick_body_ratio = 0.20;
      entry_expiry_bars = 3;
      stop_mode = STOP_OPPOSITE_EDGE;
      target_mode = TARGET_R_MULTIPLE;
      target_rr = 2.0;
      min_setup_rr = 2.0;
      use_trend_filter = true;
      use_session_filter = false;
      max_no_zone_touch_bars = 120;
      return;
     }

   if(SymbolContains("GBPUSD"))
     {
      min_consol_bars = 16;
      max_consol_bars = 50;
      min_touches = 3;
      touch_tol_pct = 6.0;
      range_vol_buf_atr = 0.05;
      range_vol_buf_ticks = 3;
      recent_touch_window = 16;
      min_recent_boundary_touches = 1;
      max_boundary_stale_bars = 40;
      max_consol_drift_pct = 35.0;
      max_outside_closes = 2;
      max_outside_close_run = 1;
      min_box_atr = 1.4;
      max_box_atr = 4.0;
      breakout_buffer_atr = 0.05;
      min_breakout_body_atr = 0.15;
      use_volume_filter = true;
      volume_multiplier = 1.0;
      max_retest_bars = 8;
      retest_tol_pct = 15.0;
      min_catalyst_body_atr = 0.12;
      close_near_extreme_pct = 30.0;
      min_wick_body_ratio = 0.30;
      entry_expiry_bars = 5;
      stop_mode = STOP_MIDPOINT;
      target_mode = TARGET_R_MULTIPLE;
      target_rr = 2.5;
      min_setup_rr = 2.5;
      use_trend_filter = true;
      use_session_filter = true;
      max_no_zone_touch_bars = 240;
      return;
     }

   if(SymbolContains("USDCAD"))
     {
      min_consol_bars = 16;
      max_consol_bars = 60;
      min_touches = 3;
      touch_tol_pct = 6.0;
      range_vol_buf_atr = 0.15;
      range_vol_buf_ticks = 3;
      recent_touch_window = 12;
      min_recent_boundary_touches = 2;
      max_boundary_stale_bars = 30;
      max_consol_drift_pct = 35.0;
      max_outside_closes = 0;
      max_outside_close_run = 1;
      min_box_atr = 1.0;
      max_box_atr = 4.0;
      breakout_buffer_atr = 0.15;
      min_breakout_body_atr = 0.25;
      use_volume_filter = true;
      volume_multiplier = 1.2;
      max_retest_bars = 8;
      retest_tol_pct = 12.0;
      min_catalyst_body_atr = 0.30;
      close_near_extreme_pct = 25.0;
      min_wick_body_ratio = 0.30;
      entry_expiry_bars = 5;
      stop_mode = STOP_MIDPOINT;
      target_mode = TARGET_R_MULTIPLE;
      target_rr = 3.0;
      min_setup_rr = 2.5;
      use_trend_filter = true;
      use_session_filter = false;
      max_no_zone_touch_bars = 120;
      return;
     }

   if(SymbolContains("USDJPY"))
     {
      min_consol_bars = 30;
      max_consol_bars = 50;
      min_touches = 2;
      touch_tol_pct = 6.0;
      range_vol_buf_atr = 0.05;
      range_vol_buf_ticks = 8;
      recent_touch_window = 12;
      min_recent_boundary_touches = 1;
      max_boundary_stale_bars = 20;
      max_consol_drift_pct = 20.0;
      max_outside_closes = 2;
      max_outside_close_run = 2;
      min_box_atr = 1.0;
      max_box_atr = 6.0;
      breakout_buffer_atr = 0.10;
      min_breakout_body_atr = 0.25;
      use_volume_filter = false;
      volume_multiplier = 1.2;
      max_retest_bars = 20;
      retest_tol_pct = 12.0;
      min_catalyst_body_atr = 0.30;
      close_near_extreme_pct = 30.0;
      min_wick_body_ratio = 0.10;
      entry_expiry_bars = 3;
      stop_mode = STOP_MIDPOINT;
      target_mode = TARGET_R_MULTIPLE;
      target_rr = 3.0;
      min_setup_rr = 2.0;
      use_trend_filter = false;
      use_session_filter = true;
      max_no_zone_touch_bars = 60;
     }
  }

void DeleteActiveBox()
  {
   if(ObjectFind(0,BOX_OBJECT_NAME) >= 0)
      ObjectDelete(0,BOX_OBJECT_NAME);
  }

void DrawActiveBox(const datetime left_time,
                   const datetime right_time,
                   const double top_price,
                   const double bottom_price)
  {
   if(!InpShowBoxArea)
     {
      DeleteActiveBox();
      return;
     }

   if(ObjectFind(0,BOX_OBJECT_NAME) < 0)
      ObjectCreate(0,BOX_OBJECT_NAME,OBJ_RECTANGLE,0,left_time,top_price,right_time,bottom_price);
   else
     {
      ObjectMove(0,BOX_OBJECT_NAME,0,left_time,top_price);
      ObjectMove(0,BOX_OBJECT_NAME,1,right_time,bottom_price);
     }

   ObjectSetInteger(0,BOX_OBJECT_NAME,OBJPROP_COLOR,clrDarkOrange);
   ObjectSetInteger(0,BOX_OBJECT_NAME,OBJPROP_STYLE,STYLE_SOLID);
   ObjectSetInteger(0,BOX_OBJECT_NAME,OBJPROP_WIDTH,1);
   ObjectSetInteger(0,BOX_OBJECT_NAME,OBJPROP_BACK,true);
   ObjectSetInteger(0,BOX_OBJECT_NAME,OBJPROP_FILL,true);
   ObjectSetInteger(0,BOX_OBJECT_NAME,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,BOX_OBJECT_NAME,OBJPROP_HIDDEN,true);
  }

int OnInit()
  {
   SetIndexBuffer(0,g_boxTopBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,g_boxBottomBuffer,INDICATOR_DATA);
   SetIndexBuffer(2,g_supportBuffer,INDICATOR_DATA);
   SetIndexBuffer(3,g_resistanceBuffer,INDICATOR_DATA);
   SetIndexBuffer(4,g_entryBuffer,INDICATOR_DATA);
   SetIndexBuffer(5,g_stopBuffer,INDICATOR_DATA);
   SetIndexBuffer(6,g_targetBuffer,INDICATOR_DATA);
   SetIndexBuffer(7,g_bullSetupBuffer,INDICATOR_DATA);
   SetIndexBuffer(8,g_bearSetupBuffer,INDICATOR_DATA);
   SetIndexBuffer(9,g_bullEntryBuffer,INDICATOR_DATA);
   SetIndexBuffer(10,g_bearEntryBuffer,INDICATOR_DATA);
   SetIndexBuffer(11,g_cancelBuffer,INDICATOR_DATA);

   for(int i = 0; i < 12; ++i)
      PlotIndexSetDouble(i,PLOT_EMPTY_VALUE,EMPTY_VALUE);

   PlotIndexSetInteger(7,PLOT_ARROW,233);
   PlotIndexSetInteger(8,PLOT_ARROW,234);
   PlotIndexSetInteger(9,PLOT_ARROW,233);
   PlotIndexSetInteger(10,PLOT_ARROW,234);
   PlotIndexSetInteger(11,PLOT_ARROW,251);

   ArraySetAsSeries(g_boxTopBuffer,true);
   ArraySetAsSeries(g_boxBottomBuffer,true);
   ArraySetAsSeries(g_supportBuffer,true);
   ArraySetAsSeries(g_resistanceBuffer,true);
   ArraySetAsSeries(g_entryBuffer,true);
   ArraySetAsSeries(g_stopBuffer,true);
   ArraySetAsSeries(g_targetBuffer,true);
   ArraySetAsSeries(g_bullSetupBuffer,true);
   ArraySetAsSeries(g_bearSetupBuffer,true);
   ArraySetAsSeries(g_bullEntryBuffer,true);
   ArraySetAsSeries(g_bearEntryBuffer,true);
   ArraySetAsSeries(g_cancelBuffer,true);

   IndicatorSetInteger(INDICATOR_DIGITS,_Digits);
   IndicatorSetString(INDICATOR_SHORTNAME,"Last Kiss (Retouch) MT5");
   BOX_OBJECT_NAME = StringFormat("LastKissActiveBox_%I64d_%s_%d",ChartID(),_Symbol,_Period);

   g_atrHandle = iATR(_Symbol,_Period,InpAtrLen);
   g_dailySmaHandle = iMA(_Symbol,PERIOD_D1,InpDailySmaLen,0,MODE_SMA,PRICE_CLOSE);
   g_h4EmaHandle = iMA(_Symbol,PERIOD_H4,InpH4EmaLen,0,MODE_EMA,PRICE_CLOSE);

   if(g_atrHandle == INVALID_HANDLE || g_dailySmaHandle == INVALID_HANDLE || g_h4EmaHandle == INVALID_HANDLE)
      return(INIT_FAILED);

   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   DeleteActiveBox();

   if(g_atrHandle != INVALID_HANDLE)
      IndicatorRelease(g_atrHandle);
   if(g_dailySmaHandle != INVALID_HANDLE)
      IndicatorRelease(g_dailySmaHandle);
   if(g_h4EmaHandle != INVALID_HANDLE)
      IndicatorRelease(g_h4EmaHandle);
  }

int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
  {
   if(rates_total < 10)
      return(0);

   double atr_values[];
   ArraySetAsSeries(atr_values,true);
   if(CopyBuffer(g_atrHandle,0,0,rates_total,atr_values) <= 0)
      return(prev_calculated);

   ArrayInitialize(g_boxTopBuffer,EMPTY_VALUE);
   ArrayInitialize(g_boxBottomBuffer,EMPTY_VALUE);
   ArrayInitialize(g_supportBuffer,EMPTY_VALUE);
   ArrayInitialize(g_resistanceBuffer,EMPTY_VALUE);
   ArrayInitialize(g_entryBuffer,EMPTY_VALUE);
   ArrayInitialize(g_stopBuffer,EMPTY_VALUE);
   ArrayInitialize(g_targetBuffer,EMPTY_VALUE);
   ArrayInitialize(g_bullSetupBuffer,EMPTY_VALUE);
   ArrayInitialize(g_bearSetupBuffer,EMPTY_VALUE);
   ArrayInitialize(g_bullEntryBuffer,EMPTY_VALUE);
   ArrayInitialize(g_bearEntryBuffer,EMPTY_VALUE);
   ArrayInitialize(g_cancelBuffer,EMPTY_VALUE);

   int min_consol_bars = MathMax(8,InpMinConsolBars);
   int max_consol_bars = MathMax(12,InpMaxConsolBars);
   int min_touches = MathMax(1,InpMinTouches);
   double touch_tol_pct = MathMax(0.5,InpTouchTolPct);
   double range_vol_buf_atr = MathMax(0.0,InpRangeVolBufAtr);
   int range_vol_buf_ticks = MathMax(0,InpRangeVolBufTicks);
   int recent_touch_window = MathMax(1,InpRecentTouchWindow);
   int min_recent_boundary_touches = MathMax(1,InpMinRecentBoundaryTouches);
   int max_boundary_stale_bars = MathMax(1,InpMaxBoundaryStaleBars);
   double max_consol_drift_pct = MathMax(0.0,InpMaxConsolDriftPct);
   int max_outside_closes = MathMax(0,InpMaxOutsideCloses);
   int max_outside_close_run = MathMax(1,InpMaxOutsideCloseRun);
   double min_box_atr = MathMax(0.1,InpMinBoxAtr);
   double max_box_atr = MathMax(min_box_atr,InpMaxBoxAtr);
   double breakout_buffer_atr = MathMax(0.0,InpBreakoutBufferAtr);
   double min_breakout_body_atr = MathMax(0.0,InpMinBreakoutBodyAtr);
   bool use_volume_filter = InpUseVolumeFilter;
   double volume_multiplier = MathMax(0.0,InpVolumeMultiplier);
   int max_retest_bars = MathMax(1,InpMaxRetestBars);
   double retest_tol_pct = MathMax(0.0,InpRetestTolPct);
   double min_catalyst_body_atr = MathMax(0.0,InpMinCatalystBodyAtr);
   double close_near_extreme_pct = MinDouble(49.0,MathMax(1.0,InpCloseNearExtremePct));
   double min_wick_body_ratio = MathMax(0.0,InpMinWickBodyRatio);
   int entry_expiry_bars = MathMax(1,InpEntryExpiryBars);
   StopMode stop_mode = InpStopMode;
   TargetMode target_mode = InpTargetMode;
   double target_rr = MathMax(2.0,InpTargetRR);
   double min_setup_rr = MathMax(2.0,InpMinSetupRR);
   bool use_trend_filter = InpUseTrendFilter;
   bool use_session_filter = InpUseSessionFilter;
   int max_no_zone_touch_bars = MathMax(1,InpMaxNoZoneTouchBars);

   ApplyPairPreset(min_consol_bars,max_consol_bars,min_touches,touch_tol_pct,range_vol_buf_atr,range_vol_buf_ticks,
                   recent_touch_window,min_recent_boundary_touches,max_boundary_stale_bars,max_consol_drift_pct,
                   max_outside_closes,max_outside_close_run,min_box_atr,max_box_atr,breakout_buffer_atr,
                   min_breakout_body_atr,use_volume_filter,volume_multiplier,max_retest_bars,retest_tol_pct,
                   min_catalyst_body_atr,close_near_extreme_pct,min_wick_body_ratio,entry_expiry_bars,stop_mode,
                   target_mode,target_rr,min_setup_rr,use_trend_filter,use_session_filter,max_no_zone_touch_bars);

   int search_min_bars = MathMin(min_consol_bars,max_consol_bars);
   int search_max_bars = MathMax(min_consol_bars,max_consol_bars);
   if(rates_total < search_max_bars + 5)
      return(0);

   const double point_size = _Point;
   const double target_zone_buffer = point_size * MathMax(0,InpTargetZoneBufferTicks);

   int state = 0;
   double box_top = 0.0;
   double box_bottom = 0.0;
   int box_start_index = -1;
   int box_right_index = -1;
   int breakout_index = -1;
   int direction = 0;
   int fake_breakouts = 0;
   double entry_price = 0.0;
   double stop_price = 0.0;
   double target_price = 0.0;
   int setup_index = -1;
   int outside_close_run = 0;
   int last_zone_touch_index = -1;
   int last_top_touch_index = -1;
   int last_bottom_touch_index = -1;
   double support_zone = EMPTY_VALUE;
   double resistance_zone = EMPTY_VALUE;

   bool lastClosedBullBreakout = false;
   bool lastClosedBearBreakout = false;
   bool lastClosedBullRetest = false;
   bool lastClosedBearRetest = false;
   bool lastClosedBullSetup = false;
   bool lastClosedBearSetup = false;
   bool lastClosedBullEntry = false;
   bool lastClosedBearEntry = false;
   bool lastClosedCanceled = false;

   for(int i = rates_total - 1; i >= 1; --i)
     {
      bool bull_breakout_event = false;
      bool bear_breakout_event = false;
      bool bull_retest_event = false;
      bool bear_retest_event = false;
      bool bull_setup_event = false;
      bool bear_setup_event = false;
      bool bull_entry_event = false;
      bool bear_entry_event = false;
      bool canceled_event = false;

      double atr = (i < ArraySize(atr_values) ? atr_values[i] : 0.0);
      if(atr <= 0.0)
         atr = point_size;

      double marker_offset = MaxDouble(atr * 0.35,point_size * 8.0);

      double pivot_low = 0.0;
      if(ConfirmedPivotLow(i,InpTargetPivotLen,rates_total,low,pivot_low))
         support_zone = pivot_low;

      double pivot_high = 0.0;
      if(ConfirmedPivotHigh(i,InpTargetPivotLen,rates_total,high,pivot_high))
         resistance_zone = pivot_high;

      bool enough_data = (i + search_max_bars - 1 < rates_total);
      int cand_len = -1;
      double cand_top = 0.0;
      double cand_bottom = 0.0;

      if(enough_data)
        {
         for(int len = search_min_bars; len <= search_max_bars; ++len)
           {
            if(i + len - 1 >= rates_total)
               break;

            double t = high[i];
            double b = low[i];
            for(int k = 1; k < len; ++k)
              {
               int idx = i + k;
               if(high[idx] > t)
                  t = high[idx];
               if(low[idx] < b)
                  b = low[idx];
              }

            double h = t - b;
            if(h <= 0.0)
               continue;

            double tol = MaxDouble(point_size * InpTouchTolTicks,h * touch_tol_pct * 0.01) + MaxDouble(point_size * range_vol_buf_ticks,atr * range_vol_buf_atr);
            int recent_len = MathMin(recent_touch_window,len);

            int top_touches = 0;
            int bottom_touches = 0;
            int top_touches_recent = 0;
            int bottom_touches_recent = 0;
            int outside_closes = 0;

            for(int k = 0; k < len; ++k)
              {
               int idx = i + k;
               if(high[idx] >= t - tol)
                  ++top_touches;
               if(low[idx] <= b + tol)
                  ++bottom_touches;
               if(close[idx] > t + tol || close[idx] < b - tol)
                  ++outside_closes;
               if(k < recent_len)
                 {
                  if(high[idx] >= t - tol)
                     ++top_touches_recent;
                  if(low[idx] <= b + tol)
                     ++bottom_touches_recent;
                 }
              }

            double drift = MathAbs(close[i] - close[i + len - 1]);
            bool height_ok = (h >= atr * min_box_atr && h <= atr * max_box_atr);
            bool touches_ok = (top_touches >= min_touches && bottom_touches >= min_touches);
            bool recent_boundary_active = (top_touches_recent >= min_recent_boundary_touches && bottom_touches_recent >= min_recent_boundary_touches);
            bool drift_ok = (drift <= h * max_consol_drift_pct * 0.01);
            bool outside_ok = (outside_closes <= max_outside_closes);

            if(height_ok && touches_ok && recent_boundary_active && drift_ok && outside_ok && len > cand_len)
              {
               cand_len = len;
               cand_top = t;
               cand_bottom = b;
              }
           }
        }

      bool candidate_valid = (cand_len > 0);

      if(state == 0 && candidate_valid)
        {
         box_top = cand_top;
         box_bottom = cand_bottom;
         box_start_index = i + cand_len - 1;
         box_right_index = i;
         breakout_index = -1;
         direction = 0;
         fake_breakouts = 0;
         entry_price = 0.0;
         stop_price = 0.0;
         target_price = 0.0;
         setup_index = -1;
         outside_close_run = 0;
         last_zone_touch_index = i;
         last_top_touch_index = i;
         last_bottom_touch_index = i;
         state = 1;
        }

      if(state == 1)
        {
         if(InpShowBox)
           {
            g_boxTopBuffer[i] = box_top;
            g_boxBottomBuffer[i] = box_bottom;
           }

         box_right_index = i;

         double active_height = box_top - box_bottom;
         double active_touch_tol = MaxDouble(point_size * InpTouchTolTicks,active_height * touch_tol_pct * 0.01) + MaxDouble(point_size * range_vol_buf_ticks,atr * range_vol_buf_atr);
         bool in_box_now = (high[i] >= box_bottom - active_touch_tol && low[i] <= box_top + active_touch_tol);
         bool top_touched_now = (high[i] >= box_top - active_touch_tol);
         bool bottom_touched_now = (low[i] <= box_bottom + active_touch_tol);
         bool close_outside_now = (close[i] > box_top + active_touch_tol || close[i] < box_bottom - active_touch_tol);

         if(in_box_now)
            last_zone_touch_index = i;
         if(top_touched_now)
            last_top_touch_index = i;
         if(bottom_touched_now)
            last_bottom_touch_index = i;
         outside_close_run = (close_outside_now ? outside_close_run + 1 : 0);

         bool inactive_too_long = (last_zone_touch_index >= 0 && (last_zone_touch_index - i > max_no_zone_touch_bars));
         bool top_stale = (last_top_touch_index >= 0 && (last_top_touch_index - i > max_boundary_stale_bars));
         bool bottom_stale = (last_bottom_touch_index >= 0 && (last_bottom_touch_index - i > max_boundary_stale_bars));
         bool stale_boundary = (top_stale || bottom_stale);
         bool outside_run_invalid = (outside_close_run > max_outside_close_run);

         if(inactive_too_long || stale_boundary || outside_run_invalid)
           {
            canceled_event = true;
            state = 0;
            box_top = 0.0;
            box_bottom = 0.0;
            box_start_index = -1;
            box_right_index = -1;
            breakout_index = -1;
            direction = 0;
            fake_breakouts = 0;
            entry_price = 0.0;
            stop_price = 0.0;
            target_price = 0.0;
            setup_index = -1;
            outside_close_run = 0;
            last_zone_touch_index = -1;
            last_top_touch_index = -1;
            last_bottom_touch_index = -1;
           }
         else
           {
            double break_buf = atr * breakout_buffer_atr;
            double volume_ma = VolumeAverage(i,InpVolumeMALength,rates_total,tick_volume);
            bool breakout_body_ok = (MathAbs(close[i] - open[i]) >= atr * min_breakout_body_atr);
            bool breakout_volume_ok = (!use_volume_filter || volume_ma <= 0.0 || (double)tick_volume[i] > volume_ma * volume_multiplier);
            bool prior_close_ok = (i + 1 < rates_total);
            bool long_break_raw = (InpBreakoutCloseOnly ? close[i] > box_top + break_buf : high[i] > box_top + break_buf);
            bool short_break_raw = (InpBreakoutCloseOnly ? close[i] < box_bottom - break_buf : low[i] < box_bottom - break_buf);
            bool long_break = (prior_close_ok && long_break_raw && close[i + 1] <= box_top && breakout_body_ok && breakout_volume_ok);
            bool short_break = (prior_close_ok && short_break_raw && close[i + 1] >= box_bottom && breakout_body_ok && breakout_volume_ok);

            if(long_break)
              {
               direction = 1;
               breakout_index = i;
               state = 2;
               bull_breakout_event = true;
               last_top_touch_index = i;
               outside_close_run = 0;
               if(InpFreezeBoxOnBreakout)
                  box_right_index = i;
              }
            else if(short_break)
              {
               direction = -1;
               breakout_index = i;
               state = 2;
               bear_breakout_event = true;
               last_bottom_touch_index = i;
               outside_close_run = 0;
               if(InpFreezeBoxOnBreakout)
                  box_right_index = i;
              }
           }
        }

      if(state == 2)
        {
         if(InpShowBox)
           {
            g_boxTopBuffer[i] = box_top;
            g_boxBottomBuffer[i] = box_bottom;
           }

         if(!InpFreezeBoxOnBreakout)
            box_right_index = i;

         double box_height = box_top - box_bottom;
         double retest_tol = MaxDouble(point_size * InpRetestTolTicks,box_height * retest_tol_pct * 0.01);
         double edge = (direction == 1 ? box_top : box_bottom);
         bool touched_edge = (high[i] >= edge - retest_tol && low[i] <= edge + retest_tol);

         if(touched_edge)
           {
            bull_retest_event = (direction == 1);
            bear_retest_event = (direction == -1);
           }

         double range = MaxDouble(high[i] - low[i],point_size);
         double body = MathAbs(close[i] - open[i]);
         bool body_ok = (body >= atr * min_catalyst_body_atr);
         bool close_near_high = ((high[i] - close[i]) <= range * close_near_extreme_pct * 0.01);
         bool close_near_low = ((close[i] - low[i]) <= range * close_near_extreme_pct * 0.01);
         double lower_wick = MathMin(open[i],close[i]) - low[i];
         double upper_wick = high[i] - MathMax(open[i],close[i]);
         bool bull_wick_ok = (lower_wick >= body * min_wick_body_ratio);
         bool bear_wick_ok = (upper_wick >= body * min_wick_body_ratio);

         bool bull_catalyst = (direction == 1 && touched_edge && close[i] > open[i] && body_ok && close_near_high && bull_wick_ok);
         bool bear_catalyst = (direction == -1 && touched_edge && close[i] < open[i] && body_ok && close_near_low && bear_wick_ok);

         bool trend_long = false;
         bool trend_short = false;
         bool trend_available = GetTrendState(time[i],trend_long,trend_short);
         bool trend_ok = (!use_trend_filter || (trend_available && (direction == 1 ? trend_long : trend_short)));
         bool session_ok = (!use_session_filter || InTradeSession(time[i],InpSessionStartHour,InpSessionStartMinute,InpSessionEndHour,InpSessionEndMinute));

         if((bull_catalyst || bear_catalyst) && trend_ok && session_ok)
           {
            entry_price = (direction == 1 ? high[i] + point_size * InpEntryOffsetTicks : low[i] - point_size * InpEntryOffsetTicks);
            double box_mid = (box_top + box_bottom) * 0.5;

            if(stop_mode == STOP_MIDPOINT)
               stop_price = box_mid;
            else if(stop_mode == STOP_OPPOSITE_EDGE)
               stop_price = (direction == 1 ? box_bottom : box_top);
            else
               stop_price = (direction == 1 ? box_bottom - atr * InpStopAtrMult : box_top + atr * InpStopAtrMult);

            double risk = MaxDouble(MathAbs(entry_price - stop_price),point_size);
            double rr_target = entry_price + (double)direction * risk * target_rr;
            double zone_target = EMPTY_VALUE;

            if(direction == 1 && resistance_zone != EMPTY_VALUE && resistance_zone > entry_price)
               zone_target = resistance_zone - target_zone_buffer;
            else if(direction == -1 && support_zone != EMPTY_VALUE && support_zone < entry_price)
               zone_target = support_zone + target_zone_buffer;

            if(target_mode == TARGET_NEAREST_ZONE && zone_target != EMPTY_VALUE)
               target_price = zone_target;
            else
               target_price = rr_target;

            double setup_rr = (direction == 1 ? (target_price - entry_price) / risk : (entry_price - target_price) / risk);

            if(setup_rr >= min_setup_rr)
              {
               setup_index = i;
               state = 3;
               bull_setup_event = (direction == 1);
               bear_setup_event = (direction == -1);

               if(InpShowEventMarkers)
                 {
                  if(direction == 1)
                     g_bullSetupBuffer[i] = low[i] - marker_offset;
                  else
                     g_bearSetupBuffer[i] = high[i] + marker_offset;
                 }
              }
            else
              {
               entry_price = 0.0;
               stop_price = 0.0;
               target_price = 0.0;
              }
           }
         else
           {
            bool failed_break = (direction == 1 ? close[i] < box_top : close[i] > box_bottom);
            bool timed_out = (breakout_index >= 0 && (breakout_index - i > max_retest_bars));

            if(failed_break || timed_out)
              {
               ++fake_breakouts;
               canceled_event = true;
               int prev_direction = direction;
               direction = 0;
               breakout_index = -1;
               entry_price = 0.0;
               stop_price = 0.0;
               target_price = 0.0;
               setup_index = -1;

               if(fake_breakouts >= MathMax(1,InpMaxFakeBreakouts))
                 {
                  state = 0;
                  box_top = 0.0;
                  box_bottom = 0.0;
                  box_start_index = -1;
                  box_right_index = -1;
                  fake_breakouts = 0;
                  outside_close_run = 0;
                  last_zone_touch_index = -1;
                  last_top_touch_index = -1;
                  last_bottom_touch_index = -1;
                 }
               else
                 {
                  state = 1;
                  last_zone_touch_index = i;
                  if(prev_direction == 1)
                     last_top_touch_index = i;
                  else if(prev_direction == -1)
                     last_bottom_touch_index = i;
                  outside_close_run = 0;
                  if(!InpFreezeBoxOnBreakout)
                     box_right_index = i;
                 }
              }
           }
        }

      if(state == 3)
        {
         if(InpShowBox)
           {
            g_boxTopBuffer[i] = box_top;
            g_boxBottomBuffer[i] = box_bottom;
           }

         if(!InpFreezeBoxOnBreakout)
            box_right_index = i;

         if(InpShowLevels)
           {
            g_entryBuffer[i] = entry_price;
            g_stopBuffer[i] = stop_price;
            g_targetBuffer[i] = target_price;
           }

         int bars_since_setup = (setup_index >= 0 ? setup_index - i : 0);
         bool entry_triggered = (direction == 1 ? high[i] >= entry_price : low[i] <= entry_price);
         bool invalid_before_trigger = (direction == 1 ? low[i] <= stop_price : high[i] >= stop_price);
         bool expired = (bars_since_setup > entry_expiry_bars);

         if(entry_triggered)
           {
            bull_entry_event = (direction == 1);
            bear_entry_event = (direction == -1);

            if(InpShowEventMarkers)
              {
               if(direction == 1)
                  g_bullEntryBuffer[i] = low[i] - marker_offset * 1.7;
               else
                  g_bearEntryBuffer[i] = high[i] + marker_offset * 1.7;
              }

            g_entryBuffer[i] = EMPTY_VALUE;
            g_stopBuffer[i] = EMPTY_VALUE;
            g_targetBuffer[i] = EMPTY_VALUE;

            state = 0;
            box_top = 0.0;
            box_bottom = 0.0;
            box_start_index = -1;
            box_right_index = -1;
            breakout_index = -1;
            direction = 0;
            fake_breakouts = 0;
            entry_price = 0.0;
            stop_price = 0.0;
            target_price = 0.0;
            setup_index = -1;
            outside_close_run = 0;
            last_zone_touch_index = -1;
            last_top_touch_index = -1;
            last_bottom_touch_index = -1;
           }
         else if(invalid_before_trigger || expired)
           {
            canceled_event = true;
            g_entryBuffer[i] = EMPTY_VALUE;
            g_stopBuffer[i] = EMPTY_VALUE;
            g_targetBuffer[i] = EMPTY_VALUE;
            state = 0;
            box_top = 0.0;
            box_bottom = 0.0;
            box_start_index = -1;
            box_right_index = -1;
            breakout_index = -1;
            direction = 0;
            fake_breakouts = 0;
            entry_price = 0.0;
            stop_price = 0.0;
            target_price = 0.0;
            setup_index = -1;
            outside_close_run = 0;
            last_zone_touch_index = -1;
            last_top_touch_index = -1;
            last_bottom_touch_index = -1;
           }
        }

      if(InpShowTargetZones)
        {
         if(support_zone != EMPTY_VALUE)
            g_supportBuffer[i] = support_zone;
         if(resistance_zone != EMPTY_VALUE)
            g_resistanceBuffer[i] = resistance_zone;
        }

      if(canceled_event && InpShowEventMarkers)
         g_cancelBuffer[i] = high[i] + marker_offset * 2.2;

      if(i == 1)
        {
         lastClosedBullBreakout = bull_breakout_event;
         lastClosedBearBreakout = bear_breakout_event;
         lastClosedBullRetest = bull_retest_event;
         lastClosedBearRetest = bear_retest_event;
         lastClosedBullSetup = bull_setup_event;
         lastClosedBearSetup = bear_setup_event;
         lastClosedBullEntry = bull_entry_event;
         lastClosedBearEntry = bear_entry_event;
         lastClosedCanceled = canceled_event;
        }
     }

   if(InpShowBox && state >= 1)
     {
      g_boxTopBuffer[0] = box_top;
      g_boxBottomBuffer[0] = box_bottom;
     }

   if(InpShowTargetZones)
     {
      if(support_zone != EMPTY_VALUE)
         g_supportBuffer[0] = support_zone;
      if(resistance_zone != EMPTY_VALUE)
         g_resistanceBuffer[0] = resistance_zone;
     }

   if(InpShowLevels && state == 3)
     {
      g_entryBuffer[0] = entry_price;
      g_stopBuffer[0] = stop_price;
      g_targetBuffer[0] = target_price;
     }

   if(state >= 1 && box_start_index >= 1)
     {
      int right_index = box_right_index;
      if(state == 1 || (state >= 2 && !InpFreezeBoxOnBreakout))
         right_index = 0;
      if(right_index < 0)
         right_index = 0;

      DrawActiveBox(time[box_start_index],time[right_index],box_top,box_bottom);
     }
   else
      DeleteActiveBox();

   static datetime last_alert_bar = 0;
   if(InpEnableAlerts && rates_total > 1 && time[1] != last_alert_bar)
     {
      if(lastClosedBullBreakout)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bull breakout detected.");
      if(lastClosedBearBreakout)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bear breakout detected.");
      if(lastClosedBullRetest)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bull retest detected.");
      if(lastClosedBearRetest)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bear retest detected.");
      if(lastClosedBullSetup)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bull setup ready (buy stop above catalyst).");
      if(lastClosedBearSetup)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bear setup ready (sell stop below catalyst).");
      if(lastClosedBullEntry)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bull entry triggered.");
      if(lastClosedBearEntry)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: bear entry triggered.");
      if(lastClosedCanceled)
         Alert(_Symbol," ",EnumToString((ENUM_TIMEFRAMES)_Period)," Last Kiss: setup canceled.");

      last_alert_bar = time[1];
     }

   return(rates_total);
  }
