#property strict

enum ManualBiasMode
  {
   BIAS_AUTO = 0,
   BIAS_BULLISH = 1,
   BIAS_BEARISH = 2,
   BIAS_NEUTRAL = 3
  };

enum ZoneType
  {
   ZONE_UNKNOWN = 0,
   ZONE_CONTINUATION = 1,
   ZONE_LAST_KISS = 2,
   ZONE_REVERSAL = 3
  };

enum ZoneState
  {
   STATE_IDLE = 0,
   STATE_ARMED = 1,
   STATE_TOUCHED = 2,
   STATE_SWEEP = 3,
   STATE_CANDIDATE = 4,
   STATE_CONFIRMED = 5,
   STATE_ALERTED = 6,
   STATE_EXPIRED = 7,
   STATE_BLOCKED = 8
  };

struct ZoneSnapshot
  {
   string            name;
   ZoneType          type;
   datetime          left_time;
   datetime          right_time;
   double            top;
   double            bottom;
   double            mid;
   double            height;
   double            distance_from_price;
   bool              active_now;
  };

struct ZoneDecision
  {
   bool              valid;
   bool              touched;
   bool              sweep_detected;
   bool              candidate;
   bool              allow_long;
   bool              allow_short;
   bool              long_signal;
   bool              short_signal;
   int               state;
   string            trigger_name;
   string            reason;
   double            entry;
   double            stop;
   double            target;
   double            risk_price;
   double            cash_risk;
   double            risk_cash_limit;
   double            suggested_lot;
   double            nearest_room_level;
  };

input string         InpAllowedSymbols             = "EURUSD,GBPUSD,USDJPY,USDCAD";
input ENUM_TIMEFRAMES InpAllowedTimeframe         = PERIOD_M30;

input int            InpSessionStartHourSofia      = 10;
input int            InpSessionStartMinuteSofia    = 0;
input int            InpSessionEndHourSofia        = 18;
input int            InpSessionEndMinuteSofia      = 0;
input int            InpServerToSofiaOffsetMinutes = 0;
input bool           InpAllowSignalsOutsideSession = false;

input double         InpRiskPerTradePct            = 0.25;
input double         InpFTMOStartBalance           = 100000.0;
input double         InpMaxDailyLossPct            = 5.0;
input double         InpMaxTotalLossPct            = 10.0;
input int            InpMaxTradesPerDay            = 2;
input int            InpMaxTradesPerWeek           = 6;
input int            InpMaxOpenPositions           = 1;

input ManualBiasMode InpManualBiasOverride         = BIAS_AUTO;
input bool           InpAllowReversalAgainstBias   = true;
input int            InpDailySMALength             = 200;
input int            InpH4EMALength                = 50;

input int            InpATRLength                  = 14;
input double         InpStopAtrBufferMult          = 0.50;
input int            InpEntryOffsetTicks           = 2;
input double         InpMinBodyPctOfRange          = 0.35;
input double         InpCloseNearExtremePct        = 25.0;
input double         InpFalseBreakPenetrationAtr   = 0.15;
input double         InpEdgeTouchToleranceAtr      = 0.10;
input double         InpZoneOvershootAtr           = 0.35;
input int            InpRecentTouchLookbackBars    = 12;
input int            InpMaxZoneRetests             = 3;
input int            InpLastKissBreakoutLookback   = 12;
input double         InpLastKissBreakoutBodyAtr    = 0.25;
input int            InpLastKissRetestMaxBars      = 6;
input bool           InpUseLineRoomFilter          = true;

input bool           InpEnableAlerts               = true;
input bool           InpEnablePushNotifications    = false;
input int            InpAlertCooldownSeconds       = 30;
input bool           InpShowDashboard              = true;

int                  g_atr_handle                  = INVALID_HANDLE;
int                  g_daily_sma_handle            = INVALID_HANDLE;
int                  g_h4_ema_handle               = INVALID_HANDLE;
datetime             g_last_bar_time               = 0;

string               g_zone_names[];
datetime             g_zone_last_signal_bar[];
int                  g_zone_last_signal_dir[];
datetime             g_zone_last_alert_time[];
int                  g_zone_last_state[];
string               g_zone_last_reason[];

string ZoneTypeToString(const ZoneType type)
  {
   switch(type)
     {
      case ZONE_CONTINUATION:
         return("CONT");
      case ZONE_LAST_KISS:
         return("LK");
      case ZONE_REVERSAL:
         return("REV");
      default:
         return("UNKNOWN");
     }
  }

string BiasToString(const ManualBiasMode bias)
  {
   switch(bias)
     {
      case BIAS_BULLISH:
         return("Bullish");
      case BIAS_BEARISH:
         return("Bearish");
      case BIAS_NEUTRAL:
         return("Neutral");
      default:
         return("Auto");
     }
  }

string StateToString(const int state)
  {
   switch(state)
     {
      case STATE_ARMED:
         return("Armed");
      case STATE_TOUCHED:
         return("Touched");
      case STATE_SWEEP:
         return("Sweep");
      case STATE_CANDIDATE:
         return("Candidate");
      case STATE_CONFIRMED:
         return("Confirmed");
      case STATE_ALERTED:
         return("Alerted");
      case STATE_EXPIRED:
         return("Expired");
      case STATE_BLOCKED:
         return("Blocked");
      default:
         return("Idle");
     }
  }

double MaxDouble(const double a,const double b)
  {
   return(a > b ? a : b);
  }

double MinDouble(const double a,const double b)
  {
   return(a < b ? a : b);
  }

string UpperString(string value)
  {
   StringToUpper(value);
   return(value);
  }

string TrimString(string value)
  {
   StringTrimLeft(value);
   StringTrimRight(value);
   return(value);
  }

bool SymbolInAllowedList(const string symbol_to_check)
  {
   string tokens[];
   int count = StringSplit(InpAllowedSymbols,',',tokens);
   string upper_symbol = UpperString(symbol_to_check);

   for(int i = 0; i < count; ++i)
     {
      string token = UpperString(TrimString(tokens[i]));
      if(token == "")
         continue;
      if(StringFind(upper_symbol,token) >= 0)
         return(true);
     }

   return(false);
  }

string CurrentSymbolToken()
  {
   string tokens[];
   int count = StringSplit(InpAllowedSymbols,',',tokens);
   string upper_symbol = UpperString(_Symbol);

   for(int i = 0; i < count; ++i)
     {
      string token = UpperString(TrimString(tokens[i]));
      if(token == "")
         continue;
      if(StringFind(upper_symbol,token) >= 0)
         return(token);
     }

   return("");
  }

bool SymbolMatches()
  {
   return(CurrentSymbolToken() != "");
  }

datetime TradeServerNow()
  {
   datetime now = TimeTradeServer();
   if(now <= 0)
      now = TimeCurrent();
   return(now);
  }

int MinutesOfDay(const datetime value)
  {
   MqlDateTime parts;
   TimeToStruct(value,parts);
   return(parts.hour * 60 + parts.min);
  }

datetime StartOfToday(const datetime value)
  {
   MqlDateTime parts;
   TimeToStruct(value,parts);
   parts.hour = 0;
   parts.min = 0;
   parts.sec = 0;
   return(StructToTime(parts));
  }

datetime StartOfWeek(const datetime value)
  {
   MqlDateTime parts;
   TimeToStruct(value,parts);
   int weekday = parts.day_of_week;
   if(weekday == 0)
      weekday = 7;
   parts.day -= (weekday - 1);
   parts.hour = 0;
   parts.min = 0;
   parts.sec = 0;
   return(StructToTime(parts));
  }

bool InTradingSession()
  {
   if(InpAllowSignalsOutsideSession)
      return(true);

   datetime sofia_now = TradeServerNow() + (InpServerToSofiaOffsetMinutes * 60);
   int now_minutes = MinutesOfDay(sofia_now);
   int start_minutes = InpSessionStartHourSofia * 60 + InpSessionStartMinuteSofia;
   int end_minutes = InpSessionEndHourSofia * 60 + InpSessionEndMinuteSofia;

   if(start_minutes <= end_minutes)
      return(now_minutes >= start_minutes && now_minutes <= end_minutes);

   return(now_minutes >= start_minutes || now_minutes <= end_minutes);
  }

bool CopyLatestBufferValue(const int handle,const int shift,double &value)
  {
   if(handle == INVALID_HANDLE)
      return(false);

   double data[];
   ArraySetAsSeries(data,true);
   if(CopyBuffer(handle,0,shift,1,data) != 1)
      return(false);

   value = data[0];
   return(true);
  }

bool CopyLatestClose(const ENUM_TIMEFRAMES timeframe,const int shift,double &value)
  {
   double data[];
   ArraySetAsSeries(data,true);
   if(CopyClose(_Symbol,timeframe,shift,1,data) != 1)
      return(false);
   value = data[0];
   return(true);
  }

ManualBiasMode DetectAutoBias()
  {
   double daily_close = 0.0;
   double daily_sma = 0.0;
   double h4_close = 0.0;
   double h4_ema = 0.0;

   if(!CopyLatestClose(PERIOD_D1,1,daily_close) ||
      !CopyLatestBufferValue(g_daily_sma_handle,1,daily_sma) ||
      !CopyLatestClose(PERIOD_H4,1,h4_close) ||
      !CopyLatestBufferValue(g_h4_ema_handle,1,h4_ema))
      return(BIAS_NEUTRAL);

   if(daily_close > daily_sma && h4_close > h4_ema)
      return(BIAS_BULLISH);
   if(daily_close < daily_sma && h4_close < h4_ema)
      return(BIAS_BEARISH);

   return(BIAS_NEUTRAL);
  }

ManualBiasMode EffectiveBias(const ManualBiasMode auto_bias)
  {
   if(InpManualBiasOverride == BIAS_AUTO)
      return(auto_bias);

   return(InpManualBiasOverride);
  }

bool IsNewBar()
  {
   datetime times[];
   ArraySetAsSeries(times,true);
   if(CopyTime(_Symbol,_Period,0,2,times) != 2)
      return(false);

   if(g_last_bar_time == 0)
     {
      g_last_bar_time = times[0];
      return(false);
     }

   if(times[0] != g_last_bar_time)
     {
      g_last_bar_time = times[0];
      return(true);
     }

   return(false);
  }

int RuntimeIndex(const string zone_name)
  {
   int size = ArraySize(g_zone_names);
   for(int i = 0; i < size; ++i)
     {
      if(g_zone_names[i] == zone_name)
         return(i);
     }

   int new_index = size;
   ArrayResize(g_zone_names,new_index + 1);
   ArrayResize(g_zone_last_signal_bar,new_index + 1);
   ArrayResize(g_zone_last_signal_dir,new_index + 1);
   ArrayResize(g_zone_last_alert_time,new_index + 1);
   ArrayResize(g_zone_last_state,new_index + 1);
   ArrayResize(g_zone_last_reason,new_index + 1);

   g_zone_names[new_index] = zone_name;
   g_zone_last_signal_bar[new_index] = 0;
   g_zone_last_signal_dir[new_index] = 0;
   g_zone_last_alert_time[new_index] = 0;
   g_zone_last_state[new_index] = STATE_IDLE;
   g_zone_last_reason[new_index] = "";
   return(new_index);
  }

bool CurrentExecutionRates(MqlRates &rates[])
  {
   ArrayResize(rates,80);
   ArraySetAsSeries(rates,true);
   int copied = CopyRates(_Symbol,InpAllowedTimeframe,0,80,rates);
   return(copied >= 20);
  }

double BarRange(const MqlRates &bar)
  {
   return(bar.high - bar.low);
  }

double BodyRange(const MqlRates &bar)
  {
   return(MathAbs(bar.close - bar.open));
  }

bool CloseNearHigh(const MqlRates &bar,const double pct)
  {
   double range = BarRange(bar);
   if(range <= 0.0)
      return(false);
   return((bar.high - bar.close) <= range * (pct * 0.01));
  }

bool CloseNearLow(const MqlRates &bar,const double pct)
  {
   double range = BarRange(bar);
   if(range <= 0.0)
      return(false);
   return((bar.close - bar.low) <= range * (pct * 0.01));
  }

bool StrongBullBar(const MqlRates &bar)
  {
   double range = BarRange(bar);
   if(range <= 0.0)
      return(false);

   return(bar.close > bar.open &&
          BodyRange(bar) >= range * InpMinBodyPctOfRange &&
          CloseNearHigh(bar,InpCloseNearExtremePct));
  }

bool StrongBearBar(const MqlRates &bar)
  {
   double range = BarRange(bar);
   if(range <= 0.0)
      return(false);

   return(bar.close < bar.open &&
          BodyRange(bar) >= range * InpMinBodyPctOfRange &&
          CloseNearLow(bar,InpCloseNearExtremePct));
  }

double EntryOffsetPrice()
  {
   return((double)InpEntryOffsetTicks * _Point);
  }

double StopBufferPrice(const double atr_value)
  {
   return(atr_value * InpStopAtrBufferMult);
  }

double EdgeTolerancePrice(const double atr_value)
  {
   return(atr_value * InpEdgeTouchToleranceAtr);
  }

double FalseBreakPenetrationPrice(const double atr_value)
  {
   return(atr_value * InpFalseBreakPenetrationAtr);
  }

double ZoneOvershootAllowance(const double atr_value)
  {
   return(atr_value * InpZoneOvershootAtr);
  }

int CountZoneTouches(const MqlRates &rates[],const int lookback,const ZoneSnapshot &zone)
  {
   int touches = 0;
   int capped = MathMin(lookback,ArraySize(rates) - 1);
   for(int i = 1; i <= capped; ++i)
     {
      if(rates[i].high >= zone.bottom && rates[i].low <= zone.top)
         ++touches;
     }
   return(touches);
  }

double TradeCashRisk(const bool is_long,const double volume,const double entry,const double stop)
  {
   double profit = 0.0;
   bool ok = OrderCalcProfit(is_long ? ORDER_TYPE_BUY : ORDER_TYPE_SELL,_Symbol,volume,entry,stop,profit);
   if(!ok)
      return(0.0);
   return(MathAbs(profit));
  }

double NormalizeVolume(const double raw_volume)
  {
   double min_volume = SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN);
   double max_volume = SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MAX);
   double step = SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP);

   if(step <= 0.0)
      return(0.0);

   double bounded = MathMax(min_volume,MathMin(max_volume,raw_volume));
   double normalized = MathFloor((bounded + 1e-12) / step) * step;
   normalized = NormalizeDouble(normalized,2);

   if(normalized < min_volume)
      return(0.0);

   return(normalized);
  }

double SuggestedLotForRisk(const bool is_long,const double entry,const double stop,const double risk_cash_limit)
  {
   double one_lot_risk = TradeCashRisk(is_long,1.0,entry,stop);
   if(one_lot_risk <= 0.0)
      return(0.0);

   double raw_volume = risk_cash_limit / one_lot_risk;
   return(NormalizeVolume(raw_volume));
  }

int OpenPositionsOnAllowedSymbols()
  {
   int count = 0;
   for(int i = PositionsTotal() - 1; i >= 0; --i)
     {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0)
         continue;
      if(!PositionSelectByTicket(ticket))
         continue;
      if(SymbolInAllowedList(PositionGetString(POSITION_SYMBOL)))
         ++count;
     }
   return(count);
  }

int EntryDealsSince(const datetime start_time)
  {
   if(!HistorySelect(start_time,TradeServerNow()))
      return(0);

   int count = 0;
   int total = HistoryDealsTotal();
   for(int i = 0; i < total; ++i)
     {
      ulong deal_ticket = HistoryDealGetTicket(i);
      if(deal_ticket == 0)
         continue;
      if(!SymbolInAllowedList(HistoryDealGetString(deal_ticket,DEAL_SYMBOL)))
         continue;
      if((ENUM_DEAL_ENTRY)HistoryDealGetInteger(deal_ticket,DEAL_ENTRY) == DEAL_ENTRY_IN)
         ++count;
     }
   return(count);
  }

double ClosedPnlSince(const datetime start_time)
  {
   if(!HistorySelect(start_time,TradeServerNow()))
      return(0.0);

   double pnl = 0.0;
   int total = HistoryDealsTotal();
   for(int i = 0; i < total; ++i)
     {
      ulong deal_ticket = HistoryDealGetTicket(i);
      if(deal_ticket == 0)
         continue;
      if(!SymbolInAllowedList(HistoryDealGetString(deal_ticket,DEAL_SYMBOL)))
         continue;

      ENUM_DEAL_ENTRY entry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(deal_ticket,DEAL_ENTRY);
      if(entry == DEAL_ENTRY_OUT || entry == DEAL_ENTRY_OUT_BY)
         pnl += HistoryDealGetDouble(deal_ticket,DEAL_PROFIT);
     }
   return(pnl);
  }

double FTMODailyReferenceBalance()
  {
   datetime today_start = StartOfToday(TradeServerNow());
   return(AccountInfoDouble(ACCOUNT_BALANCE) - ClosedPnlSince(today_start));
  }

double CurrentDailyDrawdownCash()
  {
   return(MathMax(0.0,FTMODailyReferenceBalance() - AccountInfoDouble(ACCOUNT_EQUITY)));
  }

double CurrentTotalDrawdownCash()
  {
   return(MathMax(0.0,InpFTMOStartBalance - AccountInfoDouble(ACCOUNT_EQUITY)));
  }

double NearestHorizontalLine(const bool above,const double reference_price)
  {
   double nearest = above ? DBL_MAX : -DBL_MAX;
   int total = ObjectsTotal(0,0,-1);
   for(int i = total - 1; i >= 0; --i)
     {
      string name = ObjectName(0,i,0,-1);
      if(name == "")
         continue;
      if((ENUM_OBJECT)ObjectGetInteger(0,name,OBJPROP_TYPE) != OBJ_HLINE)
         continue;

      double level = ObjectGetDouble(0,name,OBJPROP_PRICE);
      if(above)
        {
         if(level > reference_price && level < nearest)
            nearest = level;
        }
      else
        {
         if(level < reference_price && level > nearest)
            nearest = level;
        }
     }

   return(nearest);
  }

ZoneType ParseZoneType(const string name_upper)
  {
   if(StringFind(name_upper,"_CONT_") >= 0)
      return(ZONE_CONTINUATION);
   if(StringFind(name_upper,"_LK_") >= 0)
      return(ZONE_LAST_KISS);
   if(StringFind(name_upper,"_REV_") >= 0)
      return(ZONE_REVERSAL);
   return(ZONE_UNKNOWN);
  }

bool IsExecutableZoneName(const string name)
  {
   string upper = UpperString(name);
   string symbol_token = CurrentSymbolToken();
   if(StringFind(upper,"Z") != 0)
      return(false);
   if(symbol_token == "" || StringFind(upper,symbol_token) < 0)
      return(false);
   return(ParseZoneType(upper) != ZONE_UNKNOWN);
  }

bool ReadZoneFromObject(const string name,ZoneSnapshot &zone)
  {
   if((ENUM_OBJECT)ObjectGetInteger(0,name,OBJPROP_TYPE) != OBJ_RECTANGLE)
      return(false);

   double price_a = ObjectGetDouble(0,name,OBJPROP_PRICE,0);
   double price_b = ObjectGetDouble(0,name,OBJPROP_PRICE,1);
   datetime time_a = (datetime)ObjectGetInteger(0,name,OBJPROP_TIME,0);
   datetime time_b = (datetime)ObjectGetInteger(0,name,OBJPROP_TIME,1);

   if(price_a == 0.0 && price_b == 0.0)
      return(false);

   zone.name = name;
   zone.type = ParseZoneType(UpperString(name));
   zone.top = MaxDouble(price_a,price_b);
   zone.bottom = MinDouble(price_a,price_b);
   zone.mid = (zone.top + zone.bottom) * 0.5;
   zone.height = zone.top - zone.bottom;
   zone.left_time = (datetime)MathMin((long)time_a,(long)time_b);
   zone.right_time = (datetime)MathMax((long)time_a,(long)time_b);
   zone.distance_from_price = MathAbs(SymbolInfoDouble(_Symbol,SYMBOL_BID) - zone.mid);
   datetime now = TradeServerNow();
   zone.active_now = (now >= zone.left_time && now <= zone.right_time);
   return(zone.type != ZONE_UNKNOWN);
  }

bool LongContinuationCandidate(const MqlRates &bar,const ZoneSnapshot &zone,const double atr_value)
  {
   double edge_tol = EdgeTolerancePrice(atr_value);
   double penetration = FalseBreakPenetrationPrice(atr_value);
   bool edge_rejection = bar.low <= zone.bottom + edge_tol && bar.close > zone.mid && StrongBullBar(bar);
   bool false_break_reclaim = bar.low < zone.bottom - penetration && bar.close > zone.bottom && StrongBullBar(bar);
   return(edge_rejection || false_break_reclaim);
  }

bool ShortContinuationCandidate(const MqlRates &bar,const ZoneSnapshot &zone,const double atr_value)
  {
   double edge_tol = EdgeTolerancePrice(atr_value);
   double penetration = FalseBreakPenetrationPrice(atr_value);
   bool edge_rejection = bar.high >= zone.top - edge_tol && bar.close < zone.mid && StrongBearBar(bar);
   bool false_break_reclaim = bar.high > zone.top + penetration && bar.close < zone.top && StrongBearBar(bar);
   return(edge_rejection || false_break_reclaim);
  }

int FindBreakoutBarLong(const MqlRates &rates[],const ZoneSnapshot &zone,const double atr_value)
  {
   int limit = MathMin(InpLastKissBreakoutLookback,ArraySize(rates) - 2);
   double min_body = atr_value * InpLastKissBreakoutBodyAtr;
   double buffer = FalseBreakPenetrationPrice(atr_value);

   for(int i = 2; i <= limit; ++i)
     {
      if(rates[i].close > zone.top + buffer && BodyRange(rates[i]) >= min_body && StrongBullBar(rates[i]))
         return(i);
     }
   return(-1);
  }

int FindBreakoutBarShort(const MqlRates &rates[],const ZoneSnapshot &zone,const double atr_value)
  {
   int limit = MathMin(InpLastKissBreakoutLookback,ArraySize(rates) - 2);
   double min_body = atr_value * InpLastKissBreakoutBodyAtr;
   double buffer = FalseBreakPenetrationPrice(atr_value);

   for(int i = 2; i <= limit; ++i)
     {
      if(rates[i].close < zone.bottom - buffer && BodyRange(rates[i]) >= min_body && StrongBearBar(rates[i]))
         return(i);
     }
   return(-1);
  }

bool LongLastKissCandidate(const MqlRates &rates[],const ZoneSnapshot &zone,const double atr_value)
  {
   int breakout_bar = FindBreakoutBarLong(rates,zone,atr_value);
   if(breakout_bar < 0)
      return(false);

   if(breakout_bar > InpLastKissRetestMaxBars + 1)
      return(false);

   for(int i = breakout_bar - 1; i >= 2; --i)
     {
      if(rates[i].close < zone.mid)
         return(false);
     }

   double edge_tol = EdgeTolerancePrice(atr_value);
   double overshoot = ZoneOvershootAllowance(atr_value);
   bool retest = rates[1].low <= zone.top + edge_tol && rates[1].low >= zone.bottom - overshoot;
   bool acceptance = rates[1].close > zone.top && StrongBullBar(rates[1]);
   return(retest && acceptance);
  }

bool ShortLastKissCandidate(const MqlRates &rates[],const ZoneSnapshot &zone,const double atr_value)
  {
   int breakout_bar = FindBreakoutBarShort(rates,zone,atr_value);
   if(breakout_bar < 0)
      return(false);

   if(breakout_bar > InpLastKissRetestMaxBars + 1)
      return(false);

   for(int i = breakout_bar - 1; i >= 2; --i)
     {
      if(rates[i].close > zone.mid)
         return(false);
     }

   double edge_tol = EdgeTolerancePrice(atr_value);
   double overshoot = ZoneOvershootAllowance(atr_value);
   bool retest = rates[1].high >= zone.bottom - edge_tol && rates[1].high <= zone.top + overshoot;
   bool acceptance = rates[1].close < zone.bottom && StrongBearBar(rates[1]);
   return(retest && acceptance);
  }

bool LongReversalCandidate(const MqlRates &bar,const ZoneSnapshot &zone,const double atr_value)
  {
   double penetration = FalseBreakPenetrationPrice(atr_value);
   return(bar.low < zone.bottom - penetration && bar.close > zone.bottom && StrongBullBar(bar));
  }

bool ShortReversalCandidate(const MqlRates &bar,const ZoneSnapshot &zone,const double atr_value)
  {
   double penetration = FalseBreakPenetrationPrice(atr_value);
   return(bar.high > zone.top + penetration && bar.close < zone.top && StrongBearBar(bar));
  }

void PopulateTradePlan(ZoneDecision &decision,const bool is_long,const MqlRates &signal_bar,const double atr_value)
  {
   double offset = EntryOffsetPrice();
   double stop_buffer = StopBufferPrice(atr_value);
   decision.risk_cash_limit = AccountInfoDouble(ACCOUNT_EQUITY) * (InpRiskPerTradePct * 0.01);

   if(is_long)
     {
      decision.entry = signal_bar.high + offset;
      decision.stop = signal_bar.low - stop_buffer;
      decision.risk_price = decision.entry - decision.stop;
      decision.target = decision.entry + (decision.risk_price * 2.0);
      decision.suggested_lot = SuggestedLotForRisk(true,decision.entry,decision.stop,decision.risk_cash_limit);
      decision.cash_risk = TradeCashRisk(true,decision.suggested_lot,decision.entry,decision.stop);
      decision.nearest_room_level = NearestHorizontalLine(true,decision.entry);
     }
   else
     {
      decision.entry = signal_bar.low - offset;
      decision.stop = signal_bar.high + stop_buffer;
      decision.risk_price = decision.stop - decision.entry;
      decision.target = decision.entry - (decision.risk_price * 2.0);
      decision.suggested_lot = SuggestedLotForRisk(false,decision.entry,decision.stop,decision.risk_cash_limit);
      decision.cash_risk = TradeCashRisk(false,decision.suggested_lot,decision.entry,decision.stop);
      decision.nearest_room_level = NearestHorizontalLine(false,decision.entry);
     }
  }

bool HasCleanRoom(const ZoneDecision &decision,const bool is_long)
  {
   if(!InpUseLineRoomFilter)
      return(true);

   if(decision.nearest_room_level == DBL_MAX || decision.nearest_room_level == -DBL_MAX)
      return(true);

   if(is_long)
      return((decision.nearest_room_level - decision.entry) >= (decision.risk_price * 2.0));

   return((decision.entry - decision.nearest_room_level) >= (decision.risk_price * 2.0));
  }

string FormatPrice(const double value)
  {
   return(DoubleToString(value,_Digits));
  }

string FormatCash(const double value)
  {
   return(DoubleToString(value,2));
  }

void EvaluateZone(const ZoneSnapshot &zone,
                  const MqlRates &rates[],
                  const double atr_value,
                  const ManualBiasMode effective_bias,
                  ZoneDecision &decision)
  {
   ZeroMemory(decision);
   decision.state = STATE_IDLE;
   decision.reason = "Waiting";

   if(!zone.active_now)
     {
      decision.state = STATE_EXPIRED;
      decision.reason = "Zone time window expired";
      return;
     }

   const MqlRates signal_bar = rates[1];
   const int touches = CountZoneTouches(rates,InpRecentTouchLookbackBars,zone);
   decision.touched = (signal_bar.high >= zone.bottom && signal_bar.low <= zone.top);
   decision.sweep_detected = (signal_bar.low < zone.bottom || signal_bar.high > zone.top);
   decision.allow_long = (effective_bias == BIAS_BULLISH);
   decision.allow_short = (effective_bias == BIAS_BEARISH);

   if(zone.type == ZONE_REVERSAL && InpAllowReversalAgainstBias)
     {
      decision.allow_long = true;
      decision.allow_short = true;
     }

   if(touches > InpMaxZoneRetests)
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Repeated tests weakened the zone";
      return;
     }

   if(decision.touched)
      decision.state = STATE_TOUCHED;
   else
      decision.state = STATE_ARMED;

   bool long_candidate = false;
   bool short_candidate = false;

   switch(zone.type)
     {
      case ZONE_CONTINUATION:
         long_candidate = decision.allow_long && LongContinuationCandidate(signal_bar,zone,atr_value);
         short_candidate = decision.allow_short && ShortContinuationCandidate(signal_bar,zone,atr_value);
         decision.trigger_name = "Continuation Reclaim";
         break;

      case ZONE_LAST_KISS:
         long_candidate = decision.allow_long && LongLastKissCandidate(rates,zone,atr_value);
         short_candidate = decision.allow_short && ShortLastKissCandidate(rates,zone,atr_value);
         decision.trigger_name = "Last Kiss";
         break;

      case ZONE_REVERSAL:
         long_candidate = decision.allow_long && LongReversalCandidate(signal_bar,zone,atr_value);
         short_candidate = decision.allow_short && ShortReversalCandidate(signal_bar,zone,atr_value);
         decision.trigger_name = "Reversal Reclaim";
         break;

      default:
         decision.state = STATE_BLOCKED;
         decision.reason = "Unsupported zone type";
         return;
     }

   decision.candidate = long_candidate || short_candidate;

   if(!decision.candidate)
     {
      if(zone.type != ZONE_REVERSAL && effective_bias == BIAS_NEUTRAL)
        {
         decision.state = STATE_BLOCKED;
         decision.reason = "HTF bias is neutral";
         return;
        }

      decision.reason = "Waiting for reclaim confirmation";
      return;
     }

   decision.state = STATE_CANDIDATE;

   if(long_candidate && !short_candidate)
      decision.long_signal = true;
   else if(short_candidate && !long_candidate)
      decision.short_signal = true;
   else
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Conflicting long and short trigger";
      return;
     }

   PopulateTradePlan(decision,decision.long_signal,signal_bar,atr_value);

   if(decision.risk_price <= 0.0)
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Invalid stop distance";
      return;
     }

   if(decision.suggested_lot <= 0.0)
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Stop too wide for symbol volume constraints";
      return;
     }

   if(decision.cash_risk > decision.risk_cash_limit)
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Projected risk exceeds per-trade FTMO limit";
      return;
     }

   if(!HasCleanRoom(decision,decision.long_signal))
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "No clean 2R room to next marked line";
      return;
     }

   if(OpenPositionsOnAllowedSymbols() >= InpMaxOpenPositions)
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Open position limit reached";
      return;
     }

   datetime today_start = StartOfToday(TradeServerNow());

   if(EntryDealsSince(today_start) >= InpMaxTradesPerDay)
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Daily trade limit reached";
      return;
     }

   if(EntryDealsSince(StartOfWeek(TradeServerNow())) >= InpMaxTradesPerWeek)
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Weekly trade limit reached";
      return;
     }

   if(CurrentDailyDrawdownCash() >= (FTMODailyReferenceBalance() * (InpMaxDailyLossPct * 0.01)))
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "FTMO daily loss limit reached";
      return;
     }

   if(CurrentTotalDrawdownCash() >= (InpFTMOStartBalance * (InpMaxTotalLossPct * 0.01)))
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "FTMO total loss limit reached";
      return;
     }

   if(!InTradingSession())
     {
      decision.state = STATE_BLOCKED;
      decision.reason = "Outside session window";
      return;
     }

   decision.valid = true;
   decision.state = STATE_CONFIRMED;
   decision.reason = "Trigger confirmed";
  }

ZoneSnapshot FindNearestZone()
  {
   ZoneSnapshot nearest;
   nearest.name = "";
   nearest.distance_from_price = DBL_MAX;

   int total = ObjectsTotal(0,0,-1);
   for(int i = total - 1; i >= 0; --i)
     {
      string name = ObjectName(0,i,0,-1);
      if(name == "" || !IsExecutableZoneName(name))
         continue;

      ZoneSnapshot zone;
      if(!ReadZoneFromObject(name,zone))
         continue;

      if(zone.distance_from_price < nearest.distance_from_price)
         nearest = zone;
     }

   return(nearest);
  }

void SendSignalAlert(const ZoneSnapshot &zone,const ZoneDecision &decision)
  {
   string direction = decision.long_signal ? "BUY" : "SELL";
   string text = _Symbol + " " + EnumToString(InpAllowedTimeframe) + " " + ZoneTypeToString(zone.type) +
                 " " + decision.trigger_name +
                 " confirmed: " + direction +
                 " | entry " + FormatPrice(decision.entry) +
                  " | stop " + FormatPrice(decision.stop) +
                  " | target " + FormatPrice(decision.target) +
                 " | lot " + DoubleToString(decision.suggested_lot,2) +
                 " | risk " + FormatCash(decision.cash_risk) +
                 " / " + FormatCash(decision.risk_cash_limit);

   if(InpEnableAlerts)
      Alert(text);
   if(InpEnablePushNotifications)
      SendNotification(text);
  }

void UpdateDashboard(const ManualBiasMode auto_bias,
                     const ManualBiasMode effective_bias,
                     const ZoneSnapshot &nearest_zone,
                     const ZoneDecision &nearest_decision)
  {
   if(!InpShowDashboard)
     {
      Comment("");
      return;
     }

   string zone_name = nearest_zone.name == "" ? "None" : nearest_zone.name;
   string zone_type = nearest_zone.name == "" ? "n/a" : ZoneTypeToString(nearest_zone.type);
   string state = nearest_zone.name == "" ? "n/a" : StateToString(nearest_decision.state);
   string direction = nearest_decision.long_signal ? "BUY" : (nearest_decision.short_signal ? "SELL" : "n/a");
   string entry = nearest_decision.entry > 0.0 ? FormatPrice(nearest_decision.entry) : "n/a";
   string stop = nearest_decision.stop > 0.0 ? FormatPrice(nearest_decision.stop) : "n/a";
   string target = nearest_decision.target > 0.0 ? FormatPrice(nearest_decision.target) : "n/a";
   string risk = nearest_decision.cash_risk > 0.0 ? FormatCash(nearest_decision.cash_risk) : "n/a";
   string lot = nearest_decision.suggested_lot > 0.0 ? DoubleToString(nearest_decision.suggested_lot,2) : "n/a";
   string risk_limit = nearest_decision.risk_cash_limit > 0.0 ? FormatCash(nearest_decision.risk_cash_limit) : "n/a";
   string symbol_scope = InpAllowedSymbols;
   string daily_dd = FormatCash(CurrentDailyDrawdownCash());
   string total_dd = FormatCash(CurrentTotalDrawdownCash());

   string panel =
      "Session Model Alert EA v1\n" +
      "Symbol/TF: " + _Symbol + " / " + EnumToString((ENUM_TIMEFRAMES)_Period) + "\n" +
      "Allowed Symbols: " + symbol_scope + "\n" +
      "Session: " + (InTradingSession() ? "ACTIVE" : "BLOCKED") + " (Sofia " +
      IntegerToString(InpSessionStartHourSofia) + ":" + StringFormat("%02d",InpSessionStartMinuteSofia) +
      " - " + IntegerToString(InpSessionEndHourSofia) + ":" + StringFormat("%02d",InpSessionEndMinuteSofia) + ")\n" +
      "Auto Bias: " + BiasToString(auto_bias) + " | Effective: " + BiasToString(effective_bias) + "\n" +
      "Daily DD: " + daily_dd + " | Total DD: " + total_dd + "\n" +
      "Nearest Zone: " + zone_name + " | Type: " + zone_type + "\n" +
      "State: " + state + " | Direction: " + direction + "\n" +
      "Entry: " + entry + " | Stop: " + stop + " | Target: " + target + "\n" +
      "Suggested Lot: " + lot + " | Risk: " + risk + " / " + risk_limit + "\n" +
      "Reason: " + nearest_decision.reason;

   Comment(panel);
  }

void ProcessZones()
  {
   if(!SymbolMatches())
      return;

   if(_Period != InpAllowedTimeframe)
      return;

   MqlRates rates[];
   if(!CurrentExecutionRates(rates))
      return;

   double atr_value = 0.0;
   if(!CopyLatestBufferValue(g_atr_handle,1,atr_value) || atr_value <= 0.0)
      return;

   ManualBiasMode auto_bias = DetectAutoBias();
   ManualBiasMode effective_bias = EffectiveBias(auto_bias);

   ZoneSnapshot nearest_zone = FindNearestZone();
   ZoneDecision nearest_decision;
   ZeroMemory(nearest_decision);
   nearest_decision.reason = "No executable zones found";

   int total = ObjectsTotal(0,0,-1);
   for(int i = total - 1; i >= 0; --i)
     {
      string name = ObjectName(0,i,0,-1);
      if(name == "" || !IsExecutableZoneName(name))
         continue;

      ZoneSnapshot zone;
      if(!ReadZoneFromObject(name,zone))
         continue;

      ZoneDecision decision;
      EvaluateZone(zone,rates,atr_value,effective_bias,decision);

      int idx = RuntimeIndex(zone.name);
      g_zone_last_state[idx] = decision.state;
      g_zone_last_reason[idx] = decision.reason;

      if(nearest_zone.name == zone.name)
         nearest_decision = decision;

      if(!decision.valid)
         continue;

      int signal_dir = decision.long_signal ? 1 : -1;
      datetime signal_bar_time = rates[1].time;
      datetime now = TradeServerNow();

      bool same_bar = (g_zone_last_signal_bar[idx] == signal_bar_time && g_zone_last_signal_dir[idx] == signal_dir);
      bool cooldown_active = (g_zone_last_alert_time[idx] > 0 &&
                              (now - g_zone_last_alert_time[idx]) < InpAlertCooldownSeconds);

      if(same_bar || cooldown_active)
         continue;

      SendSignalAlert(zone,decision);
      g_zone_last_signal_bar[idx] = signal_bar_time;
      g_zone_last_signal_dir[idx] = signal_dir;
      g_zone_last_alert_time[idx] = now;
      g_zone_last_state[idx] = STATE_ALERTED;
      g_zone_last_reason[idx] = "Alert sent";

      if(nearest_zone.name == zone.name)
        {
         nearest_decision.state = STATE_ALERTED;
         nearest_decision.reason = "Alert sent";
        }
     }

   UpdateDashboard(auto_bias,effective_bias,nearest_zone,nearest_decision);
  }

int OnInit()
  {
   g_atr_handle = iATR(_Symbol,InpAllowedTimeframe,InpATRLength);
   g_daily_sma_handle = iMA(_Symbol,PERIOD_D1,InpDailySMALength,0,MODE_SMA,PRICE_CLOSE);
   g_h4_ema_handle = iMA(_Symbol,PERIOD_H4,InpH4EMALength,0,MODE_EMA,PRICE_CLOSE);

   if(g_atr_handle == INVALID_HANDLE || g_daily_sma_handle == INVALID_HANDLE || g_h4_ema_handle == INVALID_HANDLE)
      return(INIT_FAILED);

   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   if(g_atr_handle != INVALID_HANDLE)
      IndicatorRelease(g_atr_handle);
   if(g_daily_sma_handle != INVALID_HANDLE)
      IndicatorRelease(g_daily_sma_handle);
   if(g_h4_ema_handle != INVALID_HANDLE)
      IndicatorRelease(g_h4_ema_handle);

   Comment("");
  }

void OnTick()
  {
   if(!SymbolMatches())
      return;

   if(_Period != InpAllowedTimeframe)
      return;

   if(IsNewBar())
      ProcessZones();
   else if(InpShowDashboard)
     {
      ZoneSnapshot nearest_zone = FindNearestZone();
      ZoneDecision blank;
      ZeroMemory(blank);
      blank.reason = nearest_zone.name == "" ? "No executable zones found" : "Waiting for next closed candle";
      ManualBiasMode auto_bias = DetectAutoBias();
      UpdateDashboard(auto_bias,EffectiveBias(auto_bias),nearest_zone,blank);
     }
  }
