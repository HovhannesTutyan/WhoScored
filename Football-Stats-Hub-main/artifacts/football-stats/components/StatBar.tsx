import React, { useEffect, useRef } from "react";
import { Animated, StyleSheet, Text, View } from "react-native";
import { useColors } from "@/hooks/useColors";

interface StatBarProps {
  label: string;
  value: number;
  maxValue?: number;
  color?: string;
  showValue?: boolean;
  suffix?: string;
  delay?: number;
}

export function StatBar({ label, value, maxValue = 100, color, showValue = true, suffix = "", delay = 0 }: StatBarProps) {
  const colors = useColors();
  const animWidth = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(animWidth, {
      toValue: value / maxValue,
      duration: 800,
      delay,
      useNativeDriver: false,
    }).start();
  }, [value, maxValue, delay]);

  const barColor = color ?? colors.primary;

  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <Text style={[styles.label, { color: colors.mutedForeground }]}>{label}</Text>
        {showValue && (
          <Text style={[styles.value, { color: colors.foreground }]}>
            {value}{suffix}
          </Text>
        )}
      </View>
      <View style={[styles.track, { backgroundColor: colors.border }]}>
        <Animated.View
          style={[
            styles.fill,
            {
              backgroundColor: barColor,
              width: animWidth.interpolate({
                inputRange: [0, 1],
                outputRange: ["0%", "100%"],
              }),
            },
          ]}
        />
      </View>
    </View>
  );
}

interface DualStatBarProps {
  label: string;
  homeValue: number;
  awayValue: number;
  homeColor: string;
  awayColor: string;
  suffix?: string;
  delay?: number;
}

export function DualStatBar({ label, homeValue, awayValue, homeColor, awayColor, suffix = "", delay = 0 }: DualStatBarProps) {
  const colors = useColors();
  const total = homeValue + awayValue;
  const homePct = total === 0 ? 0.5 : homeValue / total;
  const homeAnim = useRef(new Animated.Value(0.5)).current;

  useEffect(() => {
    Animated.timing(homeAnim, {
      toValue: homePct,
      duration: 900,
      delay,
      useNativeDriver: false,
    }).start();
  }, [homePct, delay]);

  return (
    <View style={styles.dualContainer}>
      <Text style={[styles.dualHome, { color: homeColor }]}>{homeValue}{suffix}</Text>
      <View style={styles.dualCenter}>
        <Text style={[styles.dualLabel, { color: colors.mutedForeground }]}>{label}</Text>
        <View style={[styles.dualTrack, { backgroundColor: colors.border }]}>
          <Animated.View
            style={[
              styles.dualFillHome,
              {
                backgroundColor: homeColor,
                width: homeAnim.interpolate({ inputRange: [0, 1], outputRange: ["0%", "100%"] }),
              },
            ]}
          />
        </View>
      </View>
      <Text style={[styles.dualAway, { color: awayColor }]}>{awayValue}{suffix}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 12,
  },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 5,
  },
  label: {
    fontSize: 12,
    fontFamily: "Inter_500Medium",
  },
  value: {
    fontSize: 12,
    fontFamily: "Inter_700Bold",
  },
  track: {
    height: 4,
    borderRadius: 2,
    overflow: "hidden",
  },
  fill: {
    height: "100%",
    borderRadius: 2,
  },
  dualContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 12,
    gap: 8,
  },
  dualHome: {
    width: 40,
    fontSize: 13,
    fontFamily: "Inter_700Bold",
    textAlign: "left",
  },
  dualAway: {
    width: 40,
    fontSize: 13,
    fontFamily: "Inter_700Bold",
    textAlign: "right",
  },
  dualCenter: {
    flex: 1,
    gap: 4,
  },
  dualLabel: {
    fontSize: 11,
    fontFamily: "Inter_500Medium",
    textAlign: "center",
  },
  dualTrack: {
    height: 5,
    borderRadius: 3,
    overflow: "hidden",
  },
  dualFillHome: {
    position: "absolute",
    left: 0,
    top: 0,
    bottom: 0,
    borderRadius: 3,
  },
});
