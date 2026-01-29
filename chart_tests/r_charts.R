# =============================================================================
# FlowCast Professional Chart Variations - R (FINAL)
# Publication-quality charts with numbered filenames for team review
# =============================================================================

# Load required libraries
suppressPackageStartupMessages({
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(scales)
  library(grid)
})

# =============================================================================
# CONFIGURATION
# =============================================================================

args <- commandArgs(trailingOnly = FALSE)
script_path <- sub("--file=", "", args[grep("--file=", args)])
if (length(script_path) > 0) {
  BASE_DIR <- dirname(normalizePath(script_path))
} else {
  BASE_DIR <- getwd()
}

OUTPUT_DIRS <- list(
  operating_profit = file.path(BASE_DIR, "01_operating_profit"),
  cost_breakdown = file.path(BASE_DIR, "02_cost_breakdown"),
  revenue_trends = file.path(BASE_DIR, "03_revenue_trends"),
  cumulative = file.path(BASE_DIR, "04_cumulative_analysis")
)

# High quality output settings
DPI <- 450
WIDTH <- 12
HEIGHT <- 7.5

# Color Palettes - carefully curated
PALETTES <- list(
  books_balances = c("#1B4F72", "#148F77", "#F39C12", "#E74C3C", "#8E44AD", "#2C3E50"),
  viridis = c("#440154", "#31688e", "#35b779", "#fde725", "#21918c", "#5ec962"),
  corporate_blue = c("#003f5c", "#2f4b7c", "#665191", "#a05195", "#d45087", "#f95d6a"),
  tableau = c("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948"),
  nature = c("#2271B2", "#F4A582", "#92C5DE", "#D1E5F0", "#B2182B", "#4D9221"),
  navy_gold = c("#1B365D", "#C9A227", "#2C5282", "#D4AF37", "#4A6FA5", "#E8C547"),
  teal_professional = c("#0D7377", "#14919B", "#0CABA8", "#28DF99", "#32E0C4", "#45B7D1"),
  warm_neutral = c("#5D4E37", "#8B7355", "#A69076", "#C4B098", "#D4C4B0", "#E8DDD0")
)

# Currency formatter
format_currency <- function(x) {
  ifelse(abs(x) >= 1000000,
         paste0("\u00A3", format(round(x / 1000000, 1), nsmall = 1), "M"),
         ifelse(abs(x) >= 1000,
                paste0("\u00A3", round(x / 1000, 0), "K"),
                paste0("\u00A3", round(x, 0))))
}

# =============================================================================
# PROFESSIONAL THEMES - 8 Distinct Styles
# =============================================================================

# Theme 1: Premium Corporate
theme_premium <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 22, hjust = 0,
                                margin = margin(b = 8), color = "#1a1a1a"),
      plot.subtitle = element_text(size = 13, hjust = 0,
                                   margin = margin(b = 20), color = "#555555"),
      plot.caption = element_text(size = 11, hjust = 0,
                                  margin = margin(t = 15), color = "#888888",
                                  face = "italic"),
      axis.text.x = element_text(size = 12, color = "#333333", margin = margin(t = 8)),
      axis.text.y = element_text(size = 12, color = "#333333", margin = margin(r = 8)),
      axis.title = element_text(size = 13, color = "#333333"),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "#e0e0e0", linewidth = 0.5),
      axis.line.x = element_line(color = "#555555", linewidth = 0.6),
      axis.ticks.x = element_line(color = "#555555", linewidth = 0.4),
      axis.ticks.length.x = unit(0.2, "cm"),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 12, color = "#333333"),
      legend.key.size = unit(0.6, "cm"),
      legend.spacing.x = unit(0.3, "cm"),
      legend.background = element_blank(),
      legend.margin = margin(b = 15),
      plot.margin = margin(30, 30, 25, 25),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# Theme 2: Minimal Modern
theme_minimal_modern <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 20, hjust = 0,
                                margin = margin(b = 6), color = "#2c2c2c"),
      plot.subtitle = element_text(size = 12, hjust = 0,
                                   margin = margin(b = 18), color = "#666666"),
      axis.text = element_text(size = 11, color = "#444444"),
      axis.title = element_blank(),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "#eeeeee", linewidth = 0.6),
      axis.line = element_blank(),
      axis.ticks = element_blank(),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 11),
      legend.key.size = unit(0.5, "cm"),
      legend.margin = margin(b = 12),
      plot.margin = margin(25, 25, 20, 20),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# Theme 3: Bold Executive
theme_bold_executive <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 24, hjust = 0,
                                margin = margin(t = 5, b = 10), color = "#1a1a1a"),
      plot.subtitle = element_text(size = 14, hjust = 0,
                                   margin = margin(b = 20), color = "#444444"),
      axis.text.x = element_text(size = 12, color = "#333333", margin = margin(t = 10)),
      axis.text.y = element_text(size = 12, color = "#333333", margin = margin(r = 10)),
      axis.title = element_text(size = 13, face = "bold"),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "#d0d0d0", linewidth = 0.6),
      axis.line.x = element_line(color = "#333333", linewidth = 0.8),
      axis.line.y = element_blank(),
      axis.ticks.y = element_blank(),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 12, face = "bold"),
      legend.key.size = unit(0.6, "cm"),
      legend.margin = margin(b = 15),
      plot.margin = margin(35, 30, 25, 25),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# Theme 4: Soft Gray Background
theme_soft_gray <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 20, hjust = 0,
                                margin = margin(b = 8), color = "#222222"),
      plot.subtitle = element_text(size = 12, hjust = 0,
                                   margin = margin(b = 18), color = "#555555"),
      axis.text = element_text(size = 11, color = "#333333"),
      axis.title = element_blank(),
      panel.grid.major = element_line(color = "#d8d8d8", linewidth = 0.6),
      panel.grid.minor = element_blank(),
      axis.line = element_blank(),
      axis.ticks = element_blank(),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 11),
      legend.key.size = unit(0.5, "cm"),
      legend.margin = margin(b = 12),
      plot.margin = margin(25, 25, 20, 20),
      plot.background = element_rect(fill = "#f5f5f5", color = NA),
      panel.background = element_rect(fill = "#f5f5f5", color = NA)
    )
}

# Theme 5: Data Labels Focus
theme_data_labels <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 20, hjust = 0,
                                margin = margin(b = 8), color = "#1a1a1a"),
      plot.subtitle = element_text(size = 12, hjust = 0,
                                   margin = margin(b = 18), color = "#666666"),
      axis.text.x = element_text(size = 11, color = "#333333", margin = margin(t = 8)),
      axis.text.y = element_text(size = 11, color = "#333333", margin = margin(r = 8)),
      axis.title = element_blank(),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "#e8e8e8", linewidth = 0.5),
      axis.line.x = element_line(color = "#888888", linewidth = 0.5),
      axis.ticks = element_blank(),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 11),
      legend.key.size = unit(0.5, "cm"),
      legend.margin = margin(b = 12),
      plot.margin = margin(28, 28, 22, 22),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# Theme 6: Viridis Accessible
theme_viridis_accessible <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 20, hjust = 0,
                                margin = margin(b = 8), color = "#1a1a1a"),
      plot.subtitle = element_text(size = 12, hjust = 0,
                                   margin = margin(b = 18), color = "#555555"),
      axis.text = element_text(size = 11, color = "#333333"),
      axis.title = element_text(size = 12, color = "#333333"),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "#e0e0e0", linewidth = 0.5),
      axis.line.x = element_line(color = "#555555", linewidth = 0.5),
      axis.ticks.x = element_line(color = "#555555", linewidth = 0.4),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 11),
      legend.key.size = unit(0.5, "cm"),
      legend.margin = margin(b = 12),
      plot.margin = margin(25, 25, 20, 20),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# Theme 7: Navy & Gold Executive
theme_navy_gold <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 22, hjust = 0,
                                margin = margin(b = 8), color = "#1B365D"),
      plot.subtitle = element_text(size = 13, hjust = 0,
                                   margin = margin(b = 20), color = "#4A6FA5"),
      axis.text.x = element_text(size = 12, color = "#1B365D", margin = margin(t = 8)),
      axis.text.y = element_text(size = 12, color = "#1B365D", margin = margin(r = 8)),
      axis.title = element_text(size = 13, color = "#1B365D"),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "#d8e0e8", linewidth = 0.5),
      axis.line.x = element_line(color = "#1B365D", linewidth = 0.6),
      axis.ticks.x = element_line(color = "#1B365D", linewidth = 0.4),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 12, color = "#1B365D"),
      legend.key.size = unit(0.6, "cm"),
      legend.margin = margin(b = 15),
      plot.margin = margin(30, 30, 25, 25),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# Theme 8: Teal Professional
theme_teal_pro <- function() {
  theme_minimal(base_size = 16, base_family = "sans") +
    theme(
      plot.title = element_text(face = "bold", size = 21, hjust = 0,
                                margin = margin(b = 8), color = "#0D7377"),
      plot.subtitle = element_text(size = 12, hjust = 0,
                                   margin = margin(b = 18), color = "#14919B"),
      axis.text = element_text(size = 11, color = "#333333"),
      axis.title = element_text(size = 12, color = "#0D7377"),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      panel.grid.major.y = element_line(color = "#d0e8e8", linewidth = 0.5),
      axis.line.x = element_line(color = "#0D7377", linewidth = 0.6),
      axis.ticks.x = element_line(color = "#0D7377", linewidth = 0.4),
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_blank(),
      legend.text = element_text(size = 11, color = "#0D7377"),
      legend.key.size = unit(0.5, "cm"),
      legend.margin = margin(b = 12),
      plot.margin = margin(25, 25, 20, 20),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )
}

# =============================================================================
# CHART 1: OPERATING PROFIT (Grouped Bar Chart) - 8 Variations
# =============================================================================

create_operating_profit_charts <- function(data) {
  output_dir <- OUTPUT_DIRS$operating_profit

  # Reshape data
  data_long <- data %>%
    select(month_name, gross_profit, admin_costs, operating_profit) %>%
    pivot_longer(cols = c(gross_profit, admin_costs, operating_profit),
                 names_to = "metric", values_to = "value") %>%
    mutate(
      metric = factor(metric,
                      levels = c("gross_profit", "admin_costs", "operating_profit"),
                      labels = c("Gross Profit", "Admin Costs", "Operating Profit")),
      month_name = factor(month_name, levels = data$month_name)
    )

  # Variation 1: Premium Corporate
  p1 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.85), width = 0.75) +
    scale_fill_manual(values = PALETTES$books_balances[1:3]) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.08)),
                       breaks = scales::pretty_breaks(n = 6)) +
    labs(
      title = "Monthly Operating Profit Analysis",
      subtitle = "Comparing gross profit, administrative costs, and operating profit for FY 2024",
      caption = "Source: FlowCast Financial Data",
      x = NULL, y = NULL
    ) +
    theme_premium()

  ggsave(file.path(output_dir, "r_01_premium_corporate.png"), p1,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 2: Minimal Modern
  p2 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.8), width = 0.7) +
    scale_fill_manual(values = c("#4A5568", "#718096", "#A0AEC0")) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.08))) +
    labs(
      title = "Operating Profit by Month",
      subtitle = "Financial performance breakdown across the fiscal year",
      x = NULL, y = NULL
    ) +
    theme_minimal_modern()

  ggsave(file.path(output_dir, "r_02_minimal_modern.png"), p2,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 3: Bold Executive
  p3 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.85), width = 0.75) +
    scale_fill_manual(values = c("#2D3748", "#E53E3E", "#38A169")) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.08))) +
    labs(
      title = "Operating Profit Performance",
      subtitle = "Key metrics driving financial results",
      x = NULL, y = NULL
    ) +
    theme_bold_executive()

  ggsave(file.path(output_dir, "r_03_bold_executive.png"), p3,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 4: Soft Gray Background
  p4 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.85), width = 0.75) +
    scale_fill_manual(values = PALETTES$tableau[1:3]) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.08))) +
    labs(
      title = "Profit Breakdown by Month",
      subtitle = "Three key financial metrics compared across all months",
      x = NULL, y = NULL
    ) +
    theme_soft_gray()

  ggsave(file.path(output_dir, "r_04_soft_gray.png"), p4,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "#f5f5f5")

  # Variation 5: With Data Labels
  data_summary <- data_long %>%
    filter(metric == "Operating Profit")

  p5 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.85), width = 0.75) +
    geom_text(data = data_summary,
              aes(label = format_currency(value)),
              position = position_dodge(width = 0.85),
              vjust = -0.5, size = 3.2, fontface = "bold", color = "#333333") +
    scale_fill_manual(values = PALETTES$corporate_blue[1:3]) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.12))) +
    labs(
      title = "Monthly Financial Performance",
      subtitle = "Operating profit values highlighted above bars",
      x = NULL, y = NULL
    ) +
    theme_data_labels()

  ggsave(file.path(output_dir, "r_05_data_labels.png"), p5,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 6: Viridis Accessible
  p6 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.85), width = 0.75) +
    scale_fill_manual(values = c(PALETTES$viridis[2], PALETTES$viridis[3], PALETTES$viridis[4])) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.08))) +
    labs(
      title = "Operating Profit Analysis",
      subtitle = "Colorblind-accessible financial visualization",
      x = NULL, y = NULL
    ) +
    theme_viridis_accessible()

  ggsave(file.path(output_dir, "r_06_viridis_accessible.png"), p6,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 7: Navy & Gold
  p7 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.85), width = 0.75) +
    scale_fill_manual(values = PALETTES$navy_gold[c(1, 2, 3)]) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.08))) +
    labs(
      title = "Executive Financial Summary",
      subtitle = "Monthly operating performance with key financial indicators",
      x = NULL, y = NULL
    ) +
    theme_navy_gold()

  ggsave(file.path(output_dir, "r_07_navy_gold.png"), p7,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 8: Teal Professional
  p8 <- ggplot(data_long, aes(x = month_name, y = value, fill = metric)) +
    geom_col(position = position_dodge(width = 0.85), width = 0.75) +
    scale_fill_manual(values = PALETTES$teal_professional[c(1, 3, 5)]) +
    scale_y_continuous(labels = format_currency,
                       expand = expansion(mult = c(0, 0.08))) +
    labs(
      title = "Operating Profit Dashboard",
      subtitle = "Financial metrics overview for the current fiscal year",
      x = NULL, y = NULL
    ) +
    theme_teal_pro()

  ggsave(file.path(output_dir, "r_08_teal_professional.png"), p8,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  message("  Created 8 Operating Profit R variations (r_01 to r_08)")
}

# =============================================================================
# CHART 2: COST BREAKDOWN (Donut/Pie Chart) - 8 Variations
# All use LEGEND-BASED labels (no labels on slices) for clean, professional look
# =============================================================================

create_cost_breakdown_charts <- function(data) {
  output_dir <- OUTPUT_DIRS$cost_breakdown

  data <- data %>%
    arrange(desc(percentage)) %>%
    mutate(category = factor(category, levels = category))

  total_amount <- sum(data$amount)

  # Create legend labels with percentage and amount
  legend_labels_full <- paste0(data$category, " (", data$percentage, "%, \u00A3", round(data$amount/1000, 0), "K)")
  legend_labels_pct <- paste0(data$category, " (", data$percentage, "%)")

  # Variation 1: Premium Donut - Clean legend with % and amounts
  p1 <- ggplot(data, aes(x = 2, y = percentage, fill = category)) +
    geom_col(width = 1, color = "white", linewidth = 2) +
    coord_polar(theta = "y") +
    xlim(0.5, 2.5) +
    scale_fill_manual(values = PALETTES$books_balances[1:nrow(data)],
                      labels = legend_labels_full) +
    labs(title = "Administrative Cost Breakdown", fill = NULL) +
    theme_void(base_size = 16) +
    theme(
      plot.title = element_text(face = "bold", size = 22, hjust = 0.5,
                                margin = margin(b = 20)),
      legend.position = "right",
      legend.text = element_text(size = 11),
      legend.key.size = unit(0.6, "cm"),
      legend.spacing.y = unit(0.2, "cm"),
      plot.margin = margin(25, 25, 25, 25),
      plot.background = element_rect(fill = "white", color = NA)
    ) +
    annotate("text", x = 0.5, y = 0, label = "Admin\nCosts",
             fontface = "bold", size = 7, color = "#333333")

  ggsave(file.path(output_dir, "r_01_premium_donut.png"), p1,
         width = 12, height = 8, dpi = DPI, bg = "white")

  # Variation 2: Minimal Donut with Total in center
  p2 <- ggplot(data, aes(x = 2, y = percentage, fill = category)) +
    geom_col(width = 0.85, color = "white", linewidth = 2.5) +
    coord_polar(theta = "y") +
    xlim(0.8, 2.5) +
    scale_fill_manual(values = c("#2D3748", "#4A5568", "#718096", "#A0AEC0", "#CBD5E0", "#E2E8F0", "#EDF2F7"),
                      labels = legend_labels_full) +
    labs(title = "Annual Administrative Expenses") +
    theme_void(base_size = 16) +
    theme(
      plot.title = element_text(face = "bold", size = 20, hjust = 0.5,
                                margin = margin(b = 15)),
      legend.position = "bottom",
      legend.title = element_blank(),
      legend.text = element_text(size = 10),
      legend.key.size = unit(0.5, "cm"),
      plot.margin = margin(25, 25, 25, 25),
      plot.background = element_rect(fill = "white", color = NA)
    ) +
    guides(fill = guide_legend(nrow = 3)) +
    annotate("text", x = 0.8, y = 0,
             label = paste0("\u00A3", round(total_amount / 1000, 0), "K\nTotal"),
             fontface = "bold", size = 8, color = "#2D3748", lineheight = 0.85)

  ggsave(file.path(output_dir, "r_02_minimal_total.png"), p2,
         width = 11, height = 10, dpi = DPI, bg = "white")

  # Variation 3: Horizontal Bar Chart
  data_sorted <- data %>% arrange(percentage)
  data_sorted$category <- factor(data_sorted$category, levels = data_sorted$category)

  p3 <- ggplot(data_sorted, aes(x = category, y = percentage)) +
    geom_col(fill = PALETTES$corporate_blue[1], width = 0.7) +
    geom_text(aes(label = paste0(percentage, "%")), hjust = -0.15,
              size = 5, fontface = "bold", color = "#333333") +
    coord_flip() +
    scale_y_continuous(expand = expansion(mult = c(0, 0.18))) +
    labs(
      title = "Administrative Cost Categories",
      subtitle = "Percentage distribution of total admin expenses",
      x = NULL, y = "Percentage of Total (%)"
    ) +
    theme_premium() +
    theme(
      axis.text.y = element_text(size = 12),
      panel.grid.major.y = element_blank()
    )

  ggsave(file.path(output_dir, "r_03_horizontal_bar.png"), p3,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 4: Bold Executive Donut - colorful palette, legend labels
  p4 <- ggplot(data, aes(x = 2, y = percentage, fill = category)) +
    geom_col(width = 1, color = "white", linewidth = 2) +
    coord_polar(theta = "y") +
    xlim(0.5, 2.5) +
    scale_fill_manual(values = c("#2D3748", "#E53E3E", "#38A169", "#D69E2E", "#805AD5", "#3182CE", "#DD6B20"),
                      labels = legend_labels_full) +
    labs(title = "Cost Distribution Analysis") +
    theme_void(base_size = 16) +
    theme(
      plot.title = element_text(face = "bold", size = 24, hjust = 0.5,
                                margin = margin(b = 20), color = "#1a1a1a"),
      legend.position = "right",
      legend.title = element_blank(),
      legend.text = element_text(size = 11),
      legend.key.size = unit(0.6, "cm"),
      legend.spacing.y = unit(0.2, "cm"),
      plot.margin = margin(30, 30, 30, 30),
      plot.background = element_rect(fill = "white", color = NA)
    ) +
    annotate("text", x = 0.5, y = 0, label = "FY2024",
             fontface = "bold", size = 8, color = "#2D3748")

  ggsave(file.path(output_dir, "r_04_bold_executive.png"), p4,
         width = 12, height = 8, dpi = DPI, bg = "white")

  # Variation 5: Viridis Donut - colorblind accessible
  p5 <- ggplot(data, aes(x = 2, y = percentage, fill = category)) +
    geom_col(width = 1, color = "white", linewidth = 1.5) +
    coord_polar(theta = "y") +
    xlim(0.5, 2.5) +
    scale_fill_manual(values = PALETTES$viridis[1:nrow(data)],
                      labels = legend_labels_full) +
    labs(title = "Cost Distribution by Category") +
    theme_void(base_size = 16) +
    theme(
      plot.title = element_text(face = "bold", size = 20, hjust = 0.5,
                                margin = margin(b = 20)),
      legend.position = "right",
      legend.title = element_blank(),
      legend.text = element_text(size = 11),
      legend.key.size = unit(0.6, "cm"),
      legend.spacing.y = unit(0.2, "cm"),
      plot.margin = margin(25, 25, 25, 25),
      plot.background = element_rect(fill = "white", color = NA)
    ) +
    annotate("text", x = 0.5, y = 0, label = "FY2024",
             size = 6, fontface = "bold", color = "#444444")

  ggsave(file.path(output_dir, "r_05_viridis_donut.png"), p5,
         width = 12, height = 8, dpi = DPI, bg = "white")

  # Variation 6: Ranked Bar Chart with Values
  p6 <- ggplot(data, aes(x = reorder(category, -percentage), y = percentage, fill = percentage)) +
    geom_col(width = 0.75) +
    geom_text(aes(label = paste0(percentage, "%\n\u00A3", round(amount/1000, 0), "K")),
              vjust = -0.3, size = 4, fontface = "bold", lineheight = 0.85) +
    scale_fill_gradient(low = PALETTES$corporate_blue[3],
                        high = PALETTES$corporate_blue[1], guide = "none") +
    scale_y_continuous(expand = expansion(mult = c(0, 0.2))) +
    labs(
      title = "Cost Category Distribution",
      subtitle = "Categories ranked by percentage of total admin costs",
      x = NULL, y = "Percentage (%)"
    ) +
    theme_premium() +
    theme(axis.text.x = element_text(angle = 35, hjust = 1, size = 11))

  ggsave(file.path(output_dir, "r_06_ranked_bars.png"), p6,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 7: Navy & Gold Donut - executive colors
  # Use a gradient of blues instead of alternating navy/gold
  navy_gradient <- c("#1B365D", "#2C5282", "#3D6BA8", "#5A8AC6", "#7BA3D4", "#9CBCE2", "#BDD5F0")

  p7 <- ggplot(data, aes(x = 2, y = percentage, fill = category)) +
    geom_col(width = 1, color = "white", linewidth = 2) +
    coord_polar(theta = "y") +
    xlim(0.5, 2.5) +
    scale_fill_manual(values = navy_gradient,
                      labels = legend_labels_full) +
    labs(title = "Executive Cost Summary") +
    theme_void(base_size = 16) +
    theme(
      plot.title = element_text(face = "bold", size = 22, hjust = 0.5,
                                margin = margin(b = 20), color = "#1B365D"),
      legend.position = "right",
      legend.title = element_blank(),
      legend.text = element_text(size = 11, color = "#1B365D"),
      legend.key.size = unit(0.6, "cm"),
      legend.spacing.y = unit(0.2, "cm"),
      plot.margin = margin(25, 25, 25, 25),
      plot.background = element_rect(fill = "white", color = NA)
    ) +
    annotate("text", x = 0.5, y = 0, label = paste0("\u00A3", round(total_amount/1000, 0), "K\nTotal"),
             fontface = "bold", size = 6, color = "#1B365D", lineheight = 0.9)

  ggsave(file.path(output_dir, "r_07_navy_gold.png"), p7,
         width = 12, height = 8, dpi = DPI, bg = "white")

  # Variation 8: Teal Professional Pie
  p8 <- ggplot(data, aes(x = "", y = percentage, fill = category)) +
    geom_col(width = 1, color = "white", linewidth = 2) +
    coord_polar(theta = "y") +
    scale_fill_manual(values = PALETTES$teal_professional[1:nrow(data)],
                      labels = legend_labels_pct) +
    labs(title = "Administrative Cost Distribution",
         subtitle = "FY 2024 expense allocation by category") +
    theme_void(base_size = 16) +
    theme(
      plot.title = element_text(face = "bold", size = 21, hjust = 0.5,
                                margin = margin(b = 5), color = "#0D7377"),
      plot.subtitle = element_text(size = 13, hjust = 0.5,
                                   margin = margin(b = 15), color = "#14919B"),
      legend.position = "right",
      legend.title = element_blank(),
      legend.text = element_text(size = 12, color = "#0D7377"),
      legend.key.size = unit(0.7, "cm"),
      legend.spacing.y = unit(0.3, "cm"),
      plot.margin = margin(25, 25, 25, 25),
      plot.background = element_rect(fill = "white", color = NA)
    )

  ggsave(file.path(output_dir, "r_08_teal_pie.png"), p8,
         width = 11, height = 8, dpi = DPI, bg = "white")

  message("  Created 8 Cost Breakdown R variations (r_01 to r_08)")
}

# =============================================================================
# CHART 3: REVENUE & PROFIT TRENDS (Multi-line + Forecast) - 8 Variations
# =============================================================================

create_revenue_trends_charts <- function(data) {
  output_dir <- OUTPUT_DIRS$revenue_trends

  data <- data %>%
    mutate(
      date = as.Date(date),
      month_idx = row_number(),
      is_forecast = as.logical(is_forecast)
    )

  historical <- data %>% filter(!is_forecast)
  forecast <- data %>% filter(is_forecast)

  x_labels <- data$month_name
  x_breaks <- data$month_idx

  # Variation 1: Premium Corporate with Confidence Bands
  p1 <- ggplot() +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.15, fill = PALETTES$books_balances[1]) +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = gross_profit_lower, ymax = gross_profit_upper),
                alpha = 0.15, fill = PALETTES$books_balances[2]) +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = net_profit_lower, ymax = net_profit_upper),
                alpha = 0.15, fill = PALETTES$books_balances[3]) +
    geom_line(data = historical, aes(x = month_idx, y = revenue, color = "Revenue"), linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = revenue), color = PALETTES$books_balances[1], size = 3) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit, color = "Gross Profit"), linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = gross_profit), color = PALETTES$books_balances[2], size = 3) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit, color = "Net Profit"), linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = net_profit), color = PALETTES$books_balances[3], size = 3) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = PALETTES$books_balances[1],
              linewidth = 1.1, linetype = "dashed", alpha = 0.7) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = PALETTES$books_balances[2],
              linewidth = 1.1, linetype = "dashed", alpha = 0.7) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = PALETTES$books_balances[3],
              linewidth = 1.1, linetype = "dashed", alpha = 0.7) +
    geom_vline(xintercept = max(historical$month_idx) + 0.5, linetype = "dotted",
               color = "#888888", linewidth = 0.8) +
    annotate("text", x = max(historical$month_idx) + 1.5, y = max(data$revenue) * 0.97,
             label = "Forecast", color = "#555555", size = 4.5, fontface = "italic") +
    scale_color_manual(values = setNames(PALETTES$books_balances[1:3],
                                         c("Revenue", "Gross Profit", "Net Profit"))) +
    scale_x_continuous(breaks = x_breaks, labels = x_labels) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Revenue & Profit Trends with Forecast",
      subtitle = "Historical performance (solid) and 6-month projection (dashed) with confidence intervals",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_premium() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_01_premium_forecast.png"), p1,
         width = 14, height = 7.5, dpi = DPI, bg = "white")

  # Variation 2: Minimal Modern
  p2 <- ggplot() +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.12, fill = "#4A5568") +
    geom_line(data = historical, aes(x = month_idx, y = revenue, color = "Revenue"), linewidth = 1.5) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit, color = "Gross Profit"), linewidth = 1.5) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit, color = "Net Profit"), linewidth = 1.5) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = "#4A5568",
              linewidth = 1.2, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = "#718096",
              linewidth = 1.2, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = "#A0AEC0",
              linewidth = 1.2, linetype = "dashed", alpha = 0.6) +
    geom_vline(xintercept = max(historical$month_idx) + 0.5, color = "#d0d0d0", linewidth = 0.8) +
    scale_color_manual(values = setNames(c("#4A5568", "#718096", "#A0AEC0"),
                                         c("Revenue", "Gross Profit", "Net Profit"))) +
    scale_x_continuous(breaks = x_breaks, labels = x_labels) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Financial Performance Outlook",
      subtitle = "Actual results with projected growth trajectory",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_minimal_modern() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_02_minimal_modern.png"), p2,
         width = 14, height = 7.5, dpi = DPI, bg = "white")

  # Variation 3: Bold Executive
  p3 <- ggplot() +
    annotate("rect", xmin = max(historical$month_idx) + 0.5, xmax = Inf,
             ymin = -Inf, ymax = Inf, alpha = 0.06, fill = "gray40") +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.18, fill = "#2D3748") +
    geom_line(data = historical, aes(x = month_idx, y = revenue, color = "Revenue"), linewidth = 2) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit, color = "Gross Profit"), linewidth = 2) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit, color = "Net Profit"), linewidth = 2) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = "#2D3748",
              linewidth = 1.5, linetype = "dashed", alpha = 0.5) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = "#E53E3E",
              linewidth = 1.5, linetype = "dashed", alpha = 0.5) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = "#38A169",
              linewidth = 1.5, linetype = "dashed", alpha = 0.5) +
    scale_color_manual(values = setNames(c("#2D3748", "#E53E3E", "#38A169"),
                                         c("Revenue", "Gross Profit", "Net Profit"))) +
    scale_x_continuous(breaks = x_breaks, labels = x_labels) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Revenue Trajectory Analysis",
      subtitle = "Historical data with projected trends and uncertainty bands",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_bold_executive() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_03_bold_executive.png"), p3,
         width = 14, height = 7.5, dpi = DPI, bg = "white")

  # Variation 4: Soft Gray Background
  p4 <- ggplot() +
    annotate("rect", xmin = max(historical$month_idx) + 0.5, xmax = Inf,
             ymin = -Inf, ymax = Inf, alpha = 0.08, fill = "gray50") +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.18, fill = PALETTES$tableau[1]) +
    geom_line(data = historical, aes(x = month_idx, y = revenue, color = "Revenue"), linewidth = 1.8) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit, color = "Gross Profit"), linewidth = 1.8) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit, color = "Net Profit"), linewidth = 1.8) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = PALETTES$tableau[1],
              linewidth = 1.3, linetype = "dashed", alpha = 0.5) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = PALETTES$tableau[2],
              linewidth = 1.3, linetype = "dashed", alpha = 0.5) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = PALETTES$tableau[3],
              linewidth = 1.3, linetype = "dashed", alpha = 0.5) +
    scale_color_manual(values = setNames(PALETTES$tableau[1:3],
                                         c("Revenue", "Gross Profit", "Net Profit"))) +
    scale_x_continuous(breaks = x_breaks, labels = x_labels) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Revenue Outlook",
      subtitle = "Historical data with projected trends and uncertainty bands",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_soft_gray() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_04_soft_gray.png"), p4,
         width = 14, height = 7.5, dpi = DPI, bg = "#f5f5f5")

  # Variation 5: With End Point Labels
  last_hist <- historical %>% slice_tail(n = 1)

  p5 <- ggplot() +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.12, fill = PALETTES$corporate_blue[1]) +
    geom_line(data = historical, aes(x = month_idx, y = revenue, color = "Revenue"), linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = revenue), color = PALETTES$corporate_blue[1], size = 2.5) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit, color = "Gross Profit"), linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = gross_profit), color = PALETTES$corporate_blue[2], size = 2.5) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit, color = "Net Profit"), linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = net_profit), color = PALETTES$corporate_blue[3], size = 2.5) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = PALETTES$corporate_blue[1],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = PALETTES$corporate_blue[2],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = PALETTES$corporate_blue[3],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_vline(xintercept = max(historical$month_idx) + 0.5, linetype = "dotted", color = "#888888") +
    geom_text(data = last_hist, aes(x = month_idx + 0.3, y = revenue,
                                     label = format_currency(revenue)),
              hjust = 0, size = 3.5, fontface = "bold", color = PALETTES$corporate_blue[1]) +
    scale_color_manual(values = setNames(PALETTES$corporate_blue[1:3],
                                         c("Revenue", "Gross Profit", "Net Profit"))) +
    scale_x_continuous(breaks = x_breaks, labels = x_labels,
                       expand = expansion(mult = c(0.02, 0.08))) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Financial Trends with Key Values",
      subtitle = "Latest actual values annotated at forecast transition",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_data_labels() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_05_data_labels.png"), p5,
         width = 14, height = 7.5, dpi = DPI, bg = "white")

  # Variation 6: Viridis Accessible
  p6 <- ggplot() +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.2, fill = PALETTES$viridis[2]) +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = net_profit_lower, ymax = net_profit_upper),
                alpha = 0.2, fill = PALETTES$viridis[4]) +
    geom_line(data = historical, aes(x = month_idx, y = revenue), color = PALETTES$viridis[2], linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = revenue), color = PALETTES$viridis[2], size = 3) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit), color = PALETTES$viridis[3], linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = gross_profit), color = PALETTES$viridis[3], size = 3, shape = 15) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit), color = PALETTES$viridis[4], linewidth = 1.3) +
    geom_point(data = historical, aes(x = month_idx, y = net_profit), color = PALETTES$viridis[4], size = 3, shape = 17) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = PALETTES$viridis[2],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = PALETTES$viridis[3],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = PALETTES$viridis[4],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_vline(xintercept = max(historical$month_idx) + 0.5, linetype = "dotted", color = "#888888") +
    scale_x_continuous(breaks = x_breaks, labels = x_labels) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Financial Trends & Forecast",
      subtitle = "Accessible visualization with confidence intervals for projected values",
      x = NULL, y = NULL
    ) +
    theme_viridis_accessible() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_06_viridis_accessible.png"), p6,
         width = 14, height = 7.5, dpi = DPI, bg = "white")

  # Variation 7: Navy & Gold
  p7 <- ggplot() +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.15, fill = PALETTES$navy_gold[1]) +
    geom_line(data = historical, aes(x = month_idx, y = revenue, color = "Revenue"), linewidth = 1.5) +
    geom_point(data = historical, aes(x = month_idx, y = revenue), color = PALETTES$navy_gold[1], size = 3.5) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit, color = "Gross Profit"), linewidth = 1.5) +
    geom_point(data = historical, aes(x = month_idx, y = gross_profit), color = PALETTES$navy_gold[2], size = 3.5) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit, color = "Net Profit"), linewidth = 1.5) +
    geom_point(data = historical, aes(x = month_idx, y = net_profit), color = PALETTES$navy_gold[3], size = 3.5) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = PALETTES$navy_gold[1],
              linewidth = 1.2, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = PALETTES$navy_gold[2],
              linewidth = 1.2, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = PALETTES$navy_gold[3],
              linewidth = 1.2, linetype = "dashed", alpha = 0.6) +
    geom_vline(xintercept = max(historical$month_idx) + 0.5, linetype = "dotted", color = "#1B365D", alpha = 0.5) +
    scale_color_manual(values = setNames(PALETTES$navy_gold[1:3],
                                         c("Revenue", "Gross Profit", "Net Profit"))) +
    scale_x_continuous(breaks = x_breaks, labels = x_labels) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Executive Financial Overview",
      subtitle = "Revenue and profit trends with forward projections",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_navy_gold() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_07_navy_gold.png"), p7,
         width = 14, height = 7.5, dpi = DPI, bg = "white")

  # Variation 8: Teal Professional
  p8 <- ggplot() +
    geom_ribbon(data = forecast, aes(x = month_idx, ymin = revenue_lower, ymax = revenue_upper),
                alpha = 0.15, fill = PALETTES$teal_professional[1]) +
    geom_line(data = historical, aes(x = month_idx, y = revenue, color = "Revenue"), linewidth = 1.4) +
    geom_point(data = historical, aes(x = month_idx, y = revenue), color = PALETTES$teal_professional[1], size = 3) +
    geom_line(data = historical, aes(x = month_idx, y = gross_profit, color = "Gross Profit"), linewidth = 1.4) +
    geom_point(data = historical, aes(x = month_idx, y = gross_profit), color = PALETTES$teal_professional[3], size = 3) +
    geom_line(data = historical, aes(x = month_idx, y = net_profit, color = "Net Profit"), linewidth = 1.4) +
    geom_point(data = historical, aes(x = month_idx, y = net_profit), color = PALETTES$teal_professional[5], size = 3) +
    geom_line(data = forecast, aes(x = month_idx, y = revenue), color = PALETTES$teal_professional[1],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = gross_profit), color = PALETTES$teal_professional[3],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_line(data = forecast, aes(x = month_idx, y = net_profit), color = PALETTES$teal_professional[5],
              linewidth = 1.1, linetype = "dashed", alpha = 0.6) +
    geom_vline(xintercept = max(historical$month_idx) + 0.5, linetype = "dotted", color = "#0D7377", alpha = 0.5) +
    scale_color_manual(values = setNames(PALETTES$teal_professional[c(1,3,5)],
                                         c("Revenue", "Gross Profit", "Net Profit"))) +
    scale_x_continuous(breaks = x_breaks, labels = x_labels) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Revenue & Profit Dashboard",
      subtitle = "Tracking financial metrics with 6-month forecast horizon",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_teal_pro() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 10))

  ggsave(file.path(output_dir, "r_08_teal_professional.png"), p8,
         width = 14, height = 7.5, dpi = DPI, bg = "white")

  message("  Created 8 Revenue Trends R variations (r_01 to r_08)")
}

# =============================================================================
# CHART 4: CUMULATIVE ANALYSIS (Area + Trend) - 8 Variations
# =============================================================================

create_cumulative_charts <- function(data) {
  output_dir <- OUTPUT_DIRS$cumulative

  data <- data %>%
    mutate(
      month_idx = row_number(),
      month_name = factor(month_name, levels = month_name)
    )

  # Calculate trend lines
  profit_lm <- lm(cumulative_profit ~ month_idx, data = data)
  expenses_lm <- lm(cumulative_expenses ~ month_idx, data = data)

  data <- data %>%
    mutate(
      profit_trend = predict(profit_lm),
      expenses_trend = predict(expenses_lm),
      net_position = cumulative_profit - cumulative_expenses
    )

  # Variation 1: Premium Area Chart
  p1 <- ggplot(data) +
    geom_area(aes(x = month_idx, y = cumulative_expenses), fill = PALETTES$books_balances[1], alpha = 0.25) +
    geom_area(aes(x = month_idx, y = cumulative_profit), fill = PALETTES$books_balances[2], alpha = 0.35) +
    geom_line(aes(x = month_idx, y = cumulative_profit, color = "Cumulative Profit"), linewidth = 1.5) +
    geom_line(aes(x = month_idx, y = cumulative_expenses, color = "Cumulative Expenses"), linewidth = 1.5) +
    geom_line(aes(x = month_idx, y = profit_trend), color = PALETTES$books_balances[2],
              linewidth = 1, linetype = "dashed", alpha = 0.7) +
    geom_line(aes(x = month_idx, y = expenses_trend), color = PALETTES$books_balances[1],
              linewidth = 1, linetype = "dashed", alpha = 0.7) +
    scale_color_manual(values = setNames(PALETTES$books_balances[c(2,1)],
                                         c("Cumulative Profit", "Cumulative Expenses"))) +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Cumulative Financial Performance",
      subtitle = "Year-to-date profit vs expenses with linear trend analysis (dashed lines)",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_premium()

  ggsave(file.path(output_dir, "r_01_premium_area.png"), p1,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 2: Minimal Modern
  p2 <- ggplot(data) +
    geom_area(aes(x = month_idx, y = cumulative_expenses), fill = "#718096", alpha = 0.25) +
    geom_area(aes(x = month_idx, y = cumulative_profit), fill = "#4A5568", alpha = 0.35) +
    geom_line(aes(x = month_idx, y = cumulative_profit, color = "Profit"), linewidth = 1.5) +
    geom_line(aes(x = month_idx, y = cumulative_expenses, color = "Expenses"), linewidth = 1.5) +
    geom_line(aes(x = month_idx, y = profit_trend), color = "#333333",
              linewidth = 1, linetype = "dotted") +
    scale_color_manual(values = setNames(c("#4A5568", "#718096"),
                                         c("Profit", "Expenses"))) +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Year-to-Date Financial Position",
      subtitle = "Cumulative profit and expenses with profit trend line",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_minimal_modern()

  ggsave(file.path(output_dir, "r_02_minimal_modern.png"), p2,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 3: Net Position Bar Chart
  p3 <- ggplot(data, aes(x = month_idx, y = net_position)) +
    geom_col(aes(fill = net_position >= 0), width = 0.75, alpha = 0.85) +
    geom_hline(yintercept = 0, color = "#333333", linewidth = 1) +
    geom_line(aes(y = predict(lm(net_position ~ month_idx))),
              color = "#333333", linewidth = 1.2, linetype = "dashed") +
    scale_fill_manual(values = c("TRUE" = PALETTES$corporate_blue[1],
                                 "FALSE" = PALETTES$corporate_blue[6]),
                      guide = "none") +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Net Financial Position",
      subtitle = "Monthly cumulative profit minus expenses with trend line",
      x = NULL, y = NULL
    ) +
    theme_bold_executive()

  ggsave(file.path(output_dir, "r_03_net_position.png"), p3,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 4: Soft Gray Background
  p4 <- ggplot(data) +
    geom_area(aes(x = month_idx, y = cumulative_expenses), fill = PALETTES$tableau[3], alpha = 0.35) +
    geom_area(aes(x = month_idx, y = cumulative_profit), fill = PALETTES$tableau[5], alpha = 0.5) +
    geom_line(aes(x = month_idx, y = cumulative_profit, color = "Profit"), linewidth = 2) +
    geom_line(aes(x = month_idx, y = cumulative_expenses, color = "Expenses"), linewidth = 2) +
    geom_line(aes(x = month_idx, y = profit_trend), color = "#333333",
              linewidth = 1.2, linetype = "dashed", alpha = 0.7) +
    scale_color_manual(values = setNames(c(PALETTES$tableau[5], PALETTES$tableau[3]),
                                         c("Profit", "Expenses"))) +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Running Total Analysis",
      subtitle = "Cumulative financial metrics throughout the fiscal year",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_soft_gray()

  ggsave(file.path(output_dir, "r_04_soft_gray.png"), p4,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "#f5f5f5")

  # Variation 5: Dual Metric View with Secondary Axis
  scale_factor <- max(data$cumulative_profit) / max(data$monthly_profit)

  p5 <- ggplot(data) +
    geom_col(aes(x = month_idx - 0.2, y = monthly_profit, fill = "Monthly Profit"),
             width = 0.35, alpha = 0.65) +
    geom_col(aes(x = month_idx + 0.2, y = monthly_expenses, fill = "Monthly Expenses"),
             width = 0.35, alpha = 0.65) +
    geom_line(aes(x = month_idx, y = cumulative_profit / scale_factor),
              color = PALETTES$corporate_blue[1], linewidth = 1.5) +
    geom_point(aes(x = month_idx, y = cumulative_profit / scale_factor),
               color = PALETTES$corporate_blue[1], size = 3) +
    geom_line(aes(x = month_idx, y = cumulative_expenses / scale_factor),
              color = PALETTES$corporate_blue[4], linewidth = 1.5) +
    geom_point(aes(x = month_idx, y = cumulative_expenses / scale_factor),
               color = PALETTES$corporate_blue[4], size = 3) +
    scale_fill_manual(values = c("Monthly Profit" = PALETTES$corporate_blue[1],
                                 "Monthly Expenses" = PALETTES$corporate_blue[4])) +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(
      name = "Monthly Amount",
      labels = format_currency,
      sec.axis = sec_axis(~ . * scale_factor, name = "Cumulative Amount", labels = format_currency)
    ) +
    labs(
      title = "Cumulative vs Monthly Analysis",
      subtitle = "Bars show monthly values; lines show year-to-date cumulative totals",
      x = NULL, fill = NULL
    ) +
    theme_data_labels() +
    theme(
      axis.title.y.left = element_text(size = 11, color = "#333333"),
      axis.title.y.right = element_text(size = 11, color = "#333333")
    )

  ggsave(file.path(output_dir, "r_05_dual_axis.png"), p5,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 6: Viridis Accessible
  p6 <- ggplot(data) +
    geom_ribbon(aes(x = month_idx,
                    ymin = cumulative_profit * 0.95,
                    ymax = cumulative_profit * 1.05),
                fill = PALETTES$viridis[3], alpha = 0.15) +
    geom_line(aes(x = month_idx, y = cumulative_profit), color = PALETTES$viridis[3], linewidth = 1.5) +
    geom_point(aes(x = month_idx, y = cumulative_profit), color = PALETTES$viridis[3], size = 3.5) +
    geom_line(aes(x = month_idx, y = cumulative_expenses), color = PALETTES$viridis[2], linewidth = 1.5) +
    geom_point(aes(x = month_idx, y = cumulative_expenses), color = PALETTES$viridis[2], size = 3.5, shape = 15) +
    geom_line(aes(x = month_idx, y = profit_trend), color = PALETTES$viridis[3],
              linewidth = 0.9, linetype = "dashed", alpha = 0.6) +
    geom_line(aes(x = month_idx, y = expenses_trend), color = PALETTES$viridis[2],
              linewidth = 0.9, linetype = "dashed", alpha = 0.6) +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Cumulative Financial Analysis",
      subtitle = "Colorblind-accessible visualization of year-to-date performance",
      x = NULL, y = NULL
    ) +
    theme_viridis_accessible()

  ggsave(file.path(output_dir, "r_06_viridis_accessible.png"), p6,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 7: Navy & Gold Executive
  p7 <- ggplot(data) +
    geom_area(aes(x = month_idx, y = cumulative_expenses), fill = PALETTES$navy_gold[1], alpha = 0.2) +
    geom_area(aes(x = month_idx, y = cumulative_profit), fill = PALETTES$navy_gold[2], alpha = 0.3) +
    geom_line(aes(x = month_idx, y = cumulative_profit, color = "Cumulative Profit"), linewidth = 1.6) +
    geom_point(aes(x = month_idx, y = cumulative_profit), color = PALETTES$navy_gold[2], size = 3.5) +
    geom_line(aes(x = month_idx, y = cumulative_expenses, color = "Cumulative Expenses"), linewidth = 1.6) +
    geom_point(aes(x = month_idx, y = cumulative_expenses), color = PALETTES$navy_gold[1], size = 3.5) +
    geom_line(aes(x = month_idx, y = profit_trend), color = PALETTES$navy_gold[2],
              linewidth = 1, linetype = "dashed", alpha = 0.6) +
    scale_color_manual(values = setNames(c(PALETTES$navy_gold[2], PALETTES$navy_gold[1]),
                                         c("Cumulative Profit", "Cumulative Expenses"))) +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Executive Cumulative Summary",
      subtitle = "Year-to-date financial accumulation with trend analysis",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_navy_gold()

  ggsave(file.path(output_dir, "r_07_navy_gold.png"), p7,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  # Variation 8: Teal Professional
  p8 <- ggplot(data) +
    geom_area(aes(x = month_idx, y = cumulative_expenses), fill = PALETTES$teal_professional[2], alpha = 0.25) +
    geom_area(aes(x = month_idx, y = cumulative_profit), fill = PALETTES$teal_professional[1], alpha = 0.35) +
    geom_line(aes(x = month_idx, y = cumulative_profit, color = "Profit"), linewidth = 1.5) +
    geom_line(aes(x = month_idx, y = cumulative_expenses, color = "Expenses"), linewidth = 1.5) +
    geom_line(aes(x = month_idx, y = profit_trend), color = PALETTES$teal_professional[1],
              linewidth = 1, linetype = "dashed", alpha = 0.6) +
    geom_line(aes(x = month_idx, y = expenses_trend), color = PALETTES$teal_professional[2],
              linewidth = 1, linetype = "dashed", alpha = 0.6) +
    scale_color_manual(values = setNames(c(PALETTES$teal_professional[1], PALETTES$teal_professional[2]),
                                         c("Profit", "Expenses"))) +
    scale_x_continuous(breaks = data$month_idx, labels = data$month_name) +
    scale_y_continuous(labels = format_currency) +
    labs(
      title = "Cumulative Performance Dashboard",
      subtitle = "Running totals with linear regression trend lines",
      x = NULL, y = NULL, color = NULL
    ) +
    theme_teal_pro()

  ggsave(file.path(output_dir, "r_08_teal_professional.png"), p8,
         width = WIDTH, height = HEIGHT, dpi = DPI, bg = "white")

  message("  Created 8 Cumulative Analysis R variations (r_01 to r_08)")
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

main <- function() {
  cat("============================================================\n")
  cat("FlowCast Professional Chart Generation - R (FINAL)\n")
  cat("============================================================\n\n")

  cat("Loading sample data...\n")
  monthly_data <- read.csv(file.path(BASE_DIR, "sample_data_monthly.csv"))
  admin_data <- read.csv(file.path(BASE_DIR, "sample_data_admin.csv"))
  forecast_data <- read.csv(file.path(BASE_DIR, "sample_data_forecast.csv"))
  cumulative_data <- read.csv(file.path(BASE_DIR, "sample_data_cumulative.csv"))

  cat("\nGenerating professional chart variations...\n")
  cat("Output: 8 variations x 4 chart types = 32 R charts\n\n")

  cat("1. Operating Profit charts:\n")
  create_operating_profit_charts(monthly_data)

  cat("\n2. Cost Breakdown charts:\n")
  create_cost_breakdown_charts(admin_data)

  cat("\n3. Revenue Trends charts:\n")
  create_revenue_trends_charts(forecast_data)

  cat("\n4. Cumulative Analysis charts:\n")
  create_cumulative_charts(cumulative_data)

  cat("\n============================================================\n")
  cat("R chart generation complete!\n")
  cat("Total: 32 professional variations generated\n")
  cat(paste0("Output saved to: ", BASE_DIR, "\n"))
  cat("============================================================\n")
}

main()
